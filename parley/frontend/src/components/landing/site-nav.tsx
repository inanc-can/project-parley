"use client";

import { cn } from "cn";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { FOCUS, StartRoomButton } from "./cta";
import { TRANSITION } from "./motion";

const LINKS = [
  { id: "vision", label: "Vision" },
  { id: "questions", label: "Questions" },
  { id: "faq", label: "FAQ" },
];

const STAGGER = ["delay-100", "delay-150", "delay-200", "delay-300"];

/** Which landing section is on screen, so the nav can mark where the reader is. */
function useActiveSection(enabled: boolean) {
  const [active, setActive] = useState<string | null>(null);
  useEffect(() => {
    if (!enabled) return;
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) if (e.isIntersecting) setActive(e.target.id);
      },
      { rootMargin: "-45% 0px -50% 0px" },
    );
    for (const { id } of LINKS) {
      const el = document.getElementById(id);
      if (el) io.observe(el);
    }
    return () => io.disconnect();
  }, [enabled]);
  return enabled ? active : null;
}

export function SiteNav() {
  const pathname = usePathname();
  const onHome = pathname === "/";
  const active = useActiveSection(onHome);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open]);

  const href = (id: string) => (onHome ? `#${id}` : `/#${id}`);

  return (
    <>
      <header className="pointer-events-none fixed inset-x-0 top-0 z-50 px-4">
        <nav
          aria-label="Main"
          className="pointer-events-auto mx-auto mt-6 flex w-max items-center gap-2 rounded-lg border border-line bg-background/80 p-2 pl-4 shadow-[0_8px_32px_-16px_rgb(31_45_92/0.25)] backdrop-blur-xl"
        >
          <Link
            href="/"
            aria-current={onHome ? "page" : undefined}
            className={cn("display-title rounded-sm text-xl", FOCUS)}
          >
            Parley
          </Link>
          <ul className="ml-4 hidden items-center gap-1 md:flex">
            {LINKS.map((l) => (
              <li key={l.id}>
                <a
                  href={href(l.id)}
                  aria-current={active === l.id ? "location" : undefined}
                  className={cn(
                    "rounded-sm px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-brand",
                    "aria-[current]:text-brand aria-[current]:shadow-[inset_0_-2px_0_var(--brand)]",
                    TRANSITION,
                    FOCUS,
                  )}
                >
                  {l.label}
                </a>
              </li>
            ))}
          </ul>
          <StartRoomButton size="sm" className="ml-2 hidden md:inline-flex" />
          <button
            type="button"
            aria-expanded={open}
            aria-controls="site-menu"
            aria-label={open ? "Close menu" : "Open menu"}
            onClick={() => setOpen((o) => !o)}
            className={cn(
              "relative ml-2 flex size-8 items-center justify-center rounded-sm hover:bg-accent active:scale-[0.98] md:hidden",
              TRANSITION,
              FOCUS,
            )}
          >
            {/* Two bars that rotate into an X rather than swapping icons. */}
            <span
              aria-hidden
              className={cn(
                "absolute h-0.5 w-4 rounded-full bg-foreground",
                TRANSITION,
                open ? "translate-y-0 rotate-45" : "-translate-y-1",
              )}
            />
            <span
              aria-hidden
              className={cn(
                "absolute h-0.5 w-4 rounded-full bg-foreground",
                TRANSITION,
                open ? "translate-y-0 -rotate-45" : "translate-y-1",
              )}
            />
          </button>
        </nav>
      </header>

      <div
        id="site-menu"
        inert={!open}
        className={cn(
          "fixed inset-0 z-40 flex flex-col justify-center bg-background/80 px-6 backdrop-blur-3xl md:hidden",
          TRANSITION,
          open ? "opacity-100" : "pointer-events-none opacity-0",
        )}
      >
        <ul className="flex flex-col gap-4">
          {LINKS.map((l, i) => (
            <li key={l.id} className="overflow-hidden">
              <a
                href={href(l.id)}
                onClick={() => setOpen(false)}
                className={cn(
                  "display-title block text-5xl",
                  TRANSITION,
                  FOCUS,
                  open ? `translate-y-0 opacity-100 ${STAGGER[i]}` : "translate-y-12 opacity-0",
                )}
              >
                {l.label}
              </a>
            </li>
          ))}
          <li className="overflow-hidden pt-4">
            <div
              className={cn(
                TRANSITION,
                open ? `translate-y-0 opacity-100 ${STAGGER[LINKS.length]}` : "translate-y-12 opacity-0",
              )}
            >
              <StartRoomButton />
            </div>
          </li>
        </ul>
      </div>
    </>
  );
}
