"use client";

import { cn } from "cn";
import { useEffect, useRef } from "react";

import { EASE } from "./motion";

/**
 * Large tagline whose words light up one at a time, in reading order, as each crosses a
 * trigger line 60% down the viewport. One IntersectionObserver watches every word.
 */
export function TaglineReveal({
  lines,
  accentLast = false,
  className,
}: {
  lines: string[];
  accentLast?: boolean;
  className?: string;
}) {
  const ref = useRef<HTMLParagraphElement>(null);

  useEffect(() => {
    const words = ref.current?.querySelectorAll<HTMLElement>("[data-word]");
    if (!words?.length) return;
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          // Lit once it is above the trigger line: in the band, or already scrolled past it.
          const lit = e.isIntersecting || e.boundingClientRect.top < 0;
          e.target.toggleAttribute("data-lit", lit);
        }
      },
      { rootMargin: "0px 0px -40% 0px" },
    );
    words.forEach((w) => io.observe(w));
    return () => io.disconnect();
  }, []);

  let n = 0;
  return (
    <p
      ref={ref}
      className={cn("display-title mx-auto max-w-[1040px] text-4xl sm:text-5xl lg:text-7xl", className)}
    >
      {lines.map((line, i) => (
        <span key={i} className="block">
          {line.split(" ").map((word) => (
            <span
              key={n++}
              data-word
              className={cn(
                "text-foreground/20 transition-colors duration-700",
                accentLast && i === lines.length - 1
                  ? "data-lit:text-brand motion-reduce:text-brand"
                  : "data-lit:text-foreground motion-reduce:text-foreground",
                EASE,
              )}
            >
              {word}{" "}
            </span>
          ))}
        </span>
      ))}
    </p>
  );
}
