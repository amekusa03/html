export default async function handler(req, res) {
  // 環境変数の取得（Vercel KV / Upstash / Redis Integration に対応）
  const url = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;

  if (!url || !token) {
    return res.status(500).json({ error: 'Redis / KV environment variables not configured on Vercel.' });
  }

  const isUp = req.query.up === 'true';
  const endpoint = isUp ? `${url}/incr/visitors` : `${url}/get/visitors`;

  try {
    const response = await fetch(endpoint, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errText = await response.text();
      return res.status(response.status).json({ error: errText });
    }

    const data = await response.json();
    // Upstash / Vercel KV REST API は { result: number } を返します
    const count = typeof data.result === 'number' ? data.result : parseInt(data.result || '0', 10);

    return res.status(200).json({ count });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
