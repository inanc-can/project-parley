import type { NextConfig } from "next";

// Landing-only deployment: no API behind it, and the app routes go back to the landing page.
const siteOnly = process.env.NEXT_PUBLIC_SITE_ONLY === "1";

const nextConfig: NextConfig = {
  /* config options here */
  cacheComponents: true,
  // The browser only talks to Next; /api/* is proxied to the FastAPI server.
  async rewrites() {
    if (siteOnly) return [];
    const api = process.env.PARLEY_API_URL ?? "http://127.0.0.1:8000";
    return [{ source: "/api/:path*", destination: `${api}/api/:path*` }];
  },
  async redirects() {
    if (!siteOnly) return [];
    return ["/start", "/room/:path*"].map((source) => ({
      source,
      destination: "/",
      permanent: false,
    }));
  },
  partialPrefetching: true,
  experimental: {
    agentUpgrade: "security",
    // The room assistant can take minutes (a 72B model, several tool rounds); the proxy's
    // default 30 s cut it off while the API was still working.
    proxyTimeout: 300_000,
  },
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
