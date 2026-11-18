import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  cacheComponents: true,
  // The browser only talks to Next; /api/* is proxied to the FastAPI server.
  async rewrites() {
    const api = process.env.PARLEY_API_URL ?? "http://127.0.0.1:8000";
    return [{ source: "/api/:path*", destination: `${api}/api/:path*` }];
  },
  partialPrefetching: true,
  experimental: {
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
