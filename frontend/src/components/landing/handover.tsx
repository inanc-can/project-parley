"use client";

import { cn } from "cn";
import { useEffect, useRef, useState } from "react";

import { TRANSITION } from "./motion";

const CONVERSATIONS = [
  "Haggling over a used car",
  "Disputing a hotel bill",
  "Negotiating next year's rent",
  "Booking time with a client",
  "Asking for a raise",
];

/**
 * Companion to the tagline: everyday conversations pass from "You" to "Your agent" one by one
 * as each row crosses the same trigger line the tagline's words use.
 */
export function Handover() {
  const ref = useRef<HTMLOListElement>(null);
  const [handed, setHanded] = useState<boolean[]>(() => CONVERSATIONS.map(() => false));

  useEffect(() => {
    const rows = ref.current?.querySelectorAll<HTMLElement>("[data-row]");
    if (!rows?.length) return;
    const io = new IntersectionObserver(
      (entries) => {
        setHanded((prev) => {
          const next = [...prev];
          for (const e of entries) {
            next[Number((e.target as HTMLElement).dataset.row)] =
              e.isIntersecting || e.boundingClientRect.top < 0;
          }
          return next;
        });
      },
      { rootMargin: "0px 0px -40% 0px" },
    );
    rows.forEach((r) => io.observe(r));
    return () => io.disconnect();
  }, []);

  const count = handed.filter(Boolean).length;

  return (
    <figure className="overflow-hidden rounded-lg border border-line bg-background shadow-[0_24px_64px_-32px_rgb(31_45_92/0.35)]">
      <div className="flex items-center justify-between gap-4 border-b border-line px-6 py-4">
        <span className="label-mono">Who talks</span>
        <span className="label-mono text-brand">
          {count} of {CONVERSATIONS.length} handed over
        </span>
      </div>
      <ol ref={ref}>
        {CONVERSATIONS.map((c, i) => {
          const on = handed[i];
          return (
            <li
              key={c}
              data-row={i}
              className={cn("flex items-center justify-between gap-4 px-6 py-4", i > 0 && "border-t border-line")}
            >
              <span className={cn("display-title text-lg md:text-xl", TRANSITION, on ? "text-foreground" : "text-foreground/50")}>
                {c}
              </span>
              <span
                className={cn(
                  "inline-flex shrink-0 items-center gap-2 rounded-full border py-1 pr-3 pl-1 text-xs font-medium motion-reduce:transition-none",
                  TRANSITION,
                  on ? "border-brand bg-brand text-white" : "border-line bg-background text-muted-foreground",
                )}
              >
                <span
                  aria-hidden
                  className={cn(
                    "display-title flex size-5 items-center justify-center rounded-full text-xs",
                    TRANSITION,
                    on ? "bg-white text-brand" : "bg-secondary text-foreground",
                  )}
                >
                  {on ? "A" : "Y"}
                </span>
                {on ? "Your agent" : "You"}
              </span>
            </li>
          );
        })}
      </ol>
      <figcaption className="border-t border-line bg-secondary/60 px-6 py-4 text-sm text-muted-foreground">
        Every one of these is a conversation you can play out on Parley first.
      </figcaption>
    </figure>
  );
}
