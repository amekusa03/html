import net from 'net';
import tls from 'tls';

function sendRedisTcpCommand(redisUrlStr, commandArgs) {
  return new Promise((resolve, reject) => {
    try {
      const url = new URL(redisUrlStr);
      const isTls = url.protocol === 'rediss:';
      const port = parseInt(url.port || (isTls ? '6380' : '6379'), 10);
      const host = url.hostname;
      const password = decodeURIComponent(url.password || '');

      const client = (isTls ? tls : net).connect({ host, port, rejectUnauthorized: false }, () => {
        let cmds = [];
        if (password) {
          cmds.push(['AUTH', password]);
        }
        cmds.push(commandArgs);

        let payload = '';
        for (const cmd of cmds) {
          payload += `*${cmd.length}\r\n`;
          for (const arg of cmd) {
            const str = String(arg);
            payload += `$${Buffer.byteLength(str)}\r\n${str}\r\n`;
          }
        }
        client.write(payload);
      });

      let responseBuffer = '';
      client.on('data', (chunk) => {
        responseBuffer += chunk.toString();
        // If we received bulk string or status reply
        if (responseBuffer.endsWith('\r\n')) {
          client.end();
        }
      });

      client.on('end', () => {
        // Parse RESP response
        if (responseBuffer.startsWith('+')) {
          // Simple string e.g. +OK
          resolve(responseBuffer.trim().substring(1));
        } else if (responseBuffer.startsWith('$')) {
          // Bulk string
          const firstNewline = responseBuffer.indexOf('\r\n');
          const length = parseInt(responseBuffer.substring(1, firstNewline), 10);
          if (length === -1) {
            resolve(null);
          } else {
            const data = responseBuffer.substring(firstNewline + 2, firstNewline + 2 + length);
            resolve(data);
          }
        } else if (responseBuffer.startsWith(':')) {
          const num = parseInt(responseBuffer.trim().substring(1), 10);
          resolve(num);
        } else if (responseBuffer.startsWith('-')) {
          reject(new Error(responseBuffer.trim().substring(1)));
        } else {
          resolve(responseBuffer.trim());
        }
      });

      client.on('error', (err) => reject(err));

      setTimeout(() => {
        client.destroy();
        reject(new Error('Redis connection timeout'));
      }, 5000);
    } catch (e) {
      reject(e);
    }
  });
}

export default async function handler(req, res) {
  // CORS configuration
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,POST');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, x-api-key, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const redisUrl = process.env.REDIS_URL || process.env.KV_URL;
  const restUrl = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
  const restToken = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;

  // --- GET: Fetch latest curtain and climate state ---
  if (req.method === 'GET') {
    // 1. Upstash REST API
    if (restUrl && restToken) {
      try {
        const response = await fetch(`${restUrl}/get/curtain:latest`, {
          headers: { Authorization: `Bearer ${restToken}` }
        });
        if (!response.ok) {
          const errText = await response.text();
          return res.status(response.status).json({ error: errText });
        }
        const data = await response.json();
        let payload = null;
        if (data && data.result) {
          try {
            payload = typeof data.result === 'string' ? JSON.parse(data.result) : data.result;
          } catch {
            payload = data.result;
          }
        }
        res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
        return res.status(200).json(payload || { status: 'waiting_for_data' });
      } catch (err) {
        return res.status(500).json({ error: err.message });
      }
    }

    // 2. TCP REDIS_URL
    if (redisUrl) {
      try {
        const raw = await sendRedisTcpCommand(redisUrl, ['GET', 'curtain:latest']);
        let payload = null;
        if (raw) {
          try {
            payload = JSON.parse(raw);
          } catch {
            payload = raw;
          }
        }
        res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
        return res.status(200).json(payload || { status: 'waiting_for_data' });
      } catch (err) {
        return res.status(500).json({ error: 'Redis Error: ' + err.message });
      }
    }

    return res.status(500).json({ error: 'No Redis configuration found on server.' });
  }

  // --- POST: Save latest status from ESP32 ---
  if (req.method === 'POST') {
    const headers = req.headers || {};
    const expectedKey = process.env.CURTAIN_API_KEY;
    const clientKey = headers['x-api-key'] || (headers.authorization && headers.authorization.replace(/^Bearer\s+/i, ''));

    // Check API Key if configured
    if (expectedKey && clientKey !== expectedKey) {
      return res.status(401).json({ error: 'Unauthorized: Invalid API key' });
    }

    let body = req.body;
    if (typeof body === 'string') {
      try {
        body = JSON.parse(body || '{}');
      } catch {
        return res.status(400).json({ error: 'Bad Request: Invalid JSON' });
      }
    }
    body = body || {};

    // Ensure valid json object
    if (!body || typeof body !== 'object') {
      return res.status(400).json({ error: 'Bad Request: JSON body required' });
    }

    // Standardize payload
    const record = {
      timestamp: body.timestamp || Math.floor(Date.now() / 1000),
      outdoor_temp: typeof body.outdoor_temp === 'number' ? body.outdoor_temp : null,
      indoor_temp: typeof body.indoor_temp === 'number' ? body.indoor_temp : null,
      lux: typeof body.lux === 'number' ? body.lux : null,
      curtain_state: body.curtain_state || 'UNKNOWN',
      last_action: body.last_action || 'なし',
      action_time: body.action_time || '',
      updated_at: new Date().toISOString()
    };

    const recordJson = JSON.stringify(record);

    // 1. Upstash REST API
    if (restUrl && restToken) {
      try {
        // Upstash supports POST with JSON array command e.g. ["SET", "curtain:latest", "..."]
        const response = await fetch(`${restUrl}`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${restToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(['SET', 'curtain:latest', recordJson])
        });

        if (!response.ok) {
          const errText = await response.text();
          return res.status(response.status).json({ error: errText });
        }

        return res.status(200).json({ success: true, saved: record });
      } catch (err) {
        return res.status(500).json({ error: err.message });
      }
    }

    // 2. TCP REDIS_URL
    if (redisUrl) {
      try {
        await sendRedisTcpCommand(redisUrl, ['SET', 'curtain:latest', recordJson]);
        return res.status(200).json({ success: true, saved: record });
      } catch (err) {
        return res.status(500).json({ error: 'Redis Error: ' + err.message });
      }
    }

    return res.status(500).json({ error: 'No Redis configuration found on server.' });
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
}
