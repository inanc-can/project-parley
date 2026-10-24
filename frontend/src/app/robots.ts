import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  const base = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
  // Rooms are private links; only the public pages belong in search.
  return { rules: { userAgent: "*", allow: "/", disallow: ["/room/", "/start"] }, sitemap: `${base}/sitemap.xml` };
}
