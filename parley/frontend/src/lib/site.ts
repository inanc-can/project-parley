/**
 * Landing-only deployment (the public Vercel site): the app routes redirect to the landing
 * page and calls to action say "Coming soon". Set NEXT_PUBLIC_SITE_ONLY=1 at build time.
 */
export const SITE_ONLY = process.env.NEXT_PUBLIC_SITE_ONLY === "1";
