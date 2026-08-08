import net from 'net';
import tls from 'tls';

// 以前のカウンターの引継ぎベース値
const INITIAL_OFFSET = 451;

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
        if (responseBuffer.includes('\r\n')) {
          client.end();
        }
      });

      client.on('end', () => {
        const matches = responseBuffer.match(/:(\d+)/) || responseBuffer.match(/\r\n(\d+)\r\n/);
        if (matches && matches[1]) {
          resolve(parseInt(matches[1], 10));
        } else {
          const anyDigits = responseBuffer.match(/\d+/);
          resolve(anyDigits ? parseInt(anyDigits[0], 10) : 0);
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
  const redisUrl = process.env.REDIS_URL || process.env.KV_URL;
  const restUrl = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
  const restToken = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;

  const isUp = req.query.up === 'true';

  let rawCount = 0;

  // 1. REST API の設定がある場合
  if (restUrl && restToken) {
    try {
      const endpoint = isUp ? `${restUrl}/incr/visitors` : `${restUrl}/get/visitors`;
      const response = await fetch(endpoint, {
        headers: { Authorization: `Bearer ${restToken}` }
      });
      if (!response.ok) {
        const errText = await response.text();
        return res.status(response.status).json({ error: errText });
      }
      const data = await response.json();
      rawCount = typeof data.result === 'number' ? data.result : parseInt(data.result || '0', 10);
      return res.status(200).json({ count: INITIAL_OFFSET + rawCount });
    } catch (err) {
      return res.status(500).json({ error: err.message });
    }
  }

  // 2. REDIS_URL (redis:// または rediss://) の場合
  if (redisUrl) {
    try {
      if (redisUrl.startsWith('http://') || redisUrl.startsWith('https://')) {
        const endpoint = isUp ? `${redisUrl}/incr/visitors` : `${redisUrl}/get/visitors`;
        const response = await fetch(endpoint);
        const data = await response.json();
        rawCount = typeof data.result === 'number' ? data.result : parseInt(data.result || '0', 10);
        return res.status(200).json({ count: INITIAL_OFFSET + rawCount });
      } else {
        const cmd = isUp ? ['INCR', 'visitors'] : ['GET', 'visitors'];
        rawCount = await sendRedisTcpCommand(redisUrl, cmd);
        return res.status(200).json({ count: INITIAL_OFFSET + rawCount });
      }
    } catch (err) {
      return res.status(500).json({ error: 'Redis Error: ' + err.message });
    }
  }

  return res.status(500).json({ error: 'No Redis environment variables found (REDIS_URL, etc.).' });
}
