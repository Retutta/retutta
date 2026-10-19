const ALLOWED_ORIGIN = "https://retutta.github.io";

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const headers = {
      "Access-Control-Allow-Origin": origin || ALLOWED_ORIGIN,
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store"
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers });
    }
    if (request.method !== "GET") {
      return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405, headers });
    }

    const key = "total_visits";
    const current = Number(await env.COUNTER.get(key) || "0");
    const total = current + 1;
    await env.COUNTER.put(key, String(total));
    return new Response(JSON.stringify({ total }), { status: 200, headers });
  }
};
