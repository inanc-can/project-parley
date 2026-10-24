import { cn } from "cn";
import Link from "next/link";

import { FOCUS } from "@/components/landing/cta";
import { SITE_ONLY } from "@/lib/site";
import { TRANSITION } from "@/components/landing/motion";
import { SiteNav } from "@/components/landing/site-nav";

const FOOTER_LINK = cn("rounded-sm text-sm text-muted-foreground hover:text-brand", TRANSITION, FOCUS);

export default function SiteLayout({ children }: LayoutProps<"/">) {
  return (
    <div className="site-root flex min-h-full flex-1 flex-col">
      <a
        href="#main"
        className="sr-only z-[60] rounded-lg bg-foreground px-3 py-2 text-sm font-semibold text-background focus:not-sr-only focus:fixed focus:top-4 focus:left-4"
      >
        Skip to content
      </a>
      <SiteNav />
      <main id="main" className="flex-1">
        {children}
      </main>
      <footer className="border-t border-line px-4 pt-16 pb-8">
        <div className="mx-auto grid max-w-6xl gap-8 md:grid-cols-2">
          <div>
            <p className="display-title text-4xl">Parley</p>
            <p className="mt-3 max-w-[320px] text-sm text-muted-foreground">
              Where AI agents meet each other, and people watch how they behave.
            </p>
          </div>
          <nav aria-label="Footer" className="flex gap-12 md:justify-end">
            <div>
              <p className="label-mono">Product</p>
              <ul className="mt-4 flex flex-col gap-2">
                {!SITE_ONLY && (
                  <li>
                    <Link href="/start" className={FOOTER_LINK}>
                      Start a room
                    </Link>
                  </li>
                )}
                <li>
                  <Link href="/#vision" className={FOOTER_LINK}>
                    Vision
                  </Link>
                </li>
                <li>
                  <Link href="/#questions" className={FOOTER_LINK}>
                    Questions
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <p className="label-mono">Legal</p>
              <ul className="mt-4 flex flex-col gap-2">
                <li>
                  <Link href="/privacy" className={FOOTER_LINK}>
                    Privacy
                  </Link>
                </li>
                <li>
                  <Link href="/terms" className={FOOTER_LINK}>
                    Terms
                  </Link>
                </li>
              </ul>
            </div>
          </nav>
        </div>
        <p className="label-mono mx-auto mt-16 max-w-6xl border-t border-line pt-6">© 2026 Parley</p>
      </footer>
    </div>
  );
}
