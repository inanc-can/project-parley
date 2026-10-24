"use client";

import { cn } from "cn";
import { useEffect, useState } from "react";

import { FOCUS } from "./cta";
import { EASE, TRANSITION } from "./motion";

type Scene = { title: string; a: string; b: string; watch: string[] };

// The range of the vision: the same two agents, dropped into very different situations.
const SCENES: Scene[] = [
  {
    title: "A used car sale",
    a: "I can't go under $9,150. It has a new timing belt.",
    b: "Then we're $800 apart. Shall we meet in the middle?",
    watch: ["Anchoring", "Concessions"],
  },
  {
    title: "A first date",
    a: "Honestly? I almost cancelled tonight.",
    b: "So did I. Let's skip the small talk, then.",
    watch: ["Honesty", "Rapport"],
  },
  {
    title: "Law partners settling a case",
    a: "Our client accepts the payment if the apology is public.",
    b: "A private apology, and we add six months of support.",
    watch: ["Trading issues", "Saving face"],
  },
  {
    title: "Two towns sharing a river",
    a: "We release more water in August if you cap the new dam.",
    b: "Only if the deal still holds in a dry year.",
    watch: ["Trust", "Long horizons"],
  },
  {
    title: "A salary talk",
    a: "94,000 is already the top of our band.",
    b: "Then let's talk equity, and a review in six months.",
    watch: ["Framing", "Creative options"],
  },
];

const CYCLE_MS = 5200;

export function HeroScenes() {
  const [i, setI] = useState(0);
  const [paused, setPaused] = useState(false);

  useEffect(() => {
    if (paused || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const t = setTimeout(() => setI((n) => (n + 1) % SCENES.length), CYCLE_MS);
    return () => clearTimeout(t);
  }, [i, paused]);

  const s = SCENES[i];
  const enter = cn("animate-in fade-in slide-in-from-bottom-4 fill-mode-both duration-700", EASE);

  return (
    <figure
      className="w-full"
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
      onFocus={() => setPaused(true)}
      onBlur={() => setPaused(false)}
    >
      <div className="overflow-hidden rounded-lg border border-line bg-background shadow-[0_24px_64px_-32px_rgb(31_45_92/0.35)]">
        <div className="flex items-center justify-between gap-4 border-b border-line px-6 py-4">
          <span className="label-mono">Scene</span>
          <span className="label-mono">
            {String(i + 1).padStart(2, "0")} / {String(SCENES.length).padStart(2, "0")}
          </span>
        </div>

        <div key={i} className="min-h-88 px-6 pt-8 pb-6" aria-live="polite">
          <p className={cn("display-title text-3xl md:text-4xl", enter)}>{s.title}</p>

          <div className="mt-8 flex flex-col gap-6">
            <Line who="A" label="Your agent" text={s.a} className={enter} delay={150} />
            <Line who="B" label="Their agent" text={s.b} className={enter} delay={300} right />
          </div>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-4 border-t border-line bg-secondary/60 px-6 py-4">
          <div
            key={`w${i}`}
            style={{ animationDelay: "500ms" }}
            className={cn("flex flex-wrap items-center gap-2", enter)}
          >
            <span className="label-mono mr-1">What we watch</span>
            {s.watch.map((w) => (
              <span key={w} className="rounded-sm bg-brand/10 px-2 py-0.5 text-xs text-brand">
                {w}
              </span>
            ))}
          </div>
          <div className="flex gap-1" role="group" aria-label="Choose a scene">
            {SCENES.map((sc, n) => (
              <button
                key={sc.title}
                type="button"
                aria-label={sc.title}
                aria-pressed={n === i}
                onClick={() => setI(n)}
                className={cn("flex h-6 items-center rounded-sm px-1", FOCUS)}
              >
                <span
                  className={cn(
                    "block h-1 rounded-full",
                    TRANSITION,
                    n === i ? "w-6 bg-brand" : "w-2 bg-foreground/20 hover:bg-foreground/40",
                  )}
                />
              </button>
            ))}
          </div>
        </div>
      </div>
      <figcaption className="mt-3 text-sm text-muted-foreground">
        The same two agents, five very different rooms. Illustrative lines.
      </figcaption>
    </figure>
  );
}

function Line({
  who,
  label,
  text,
  right = false,
  delay,
  className,
}: {
  who: string;
  label: string;
  text: string;
  right?: boolean;
  delay: number;
  className?: string;
}) {
  return (
    <div
      style={{ animationDelay: `${delay}ms` }}
      className={cn("flex items-start gap-3", right && "flex-row-reverse text-right", className)}
    >
      <span
        aria-hidden
        className={cn(
          "display-title flex size-10 shrink-0 items-center justify-center rounded-full text-lg",
          right ? "border border-foreground" : "bg-brand text-white",
        )}
      >
        {who}
      </span>
      <div className={cn("flex max-w-[85%] flex-col gap-1", right && "items-end")}>
        <span className="label-mono">{label}</span>
        <p
          className={cn(
            "rounded-lg px-4 py-3 text-base",
            right ? "border border-line bg-background" : "bg-secondary",
          )}
        >
          {text}
        </p>
      </div>
    </div>
  );
}
