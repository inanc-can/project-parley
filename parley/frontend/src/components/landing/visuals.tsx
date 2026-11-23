import { ArrowRightIcon, ArrowUUpLeftIcon, LockSimpleIcon, PlusIcon } from "@phosphor-icons/react/dist/ssr";
import { cn } from "cn";
import { Fragment } from "react";

// Conceptual fragments for the pillars. Decorative: the copy next to each one carries the
// meaning, so they are hidden from assistive tech.

const SCENES = [
  "A car sale",
  "A first date",
  "A lawsuit",
  "A union contract",
  "A shared river",
  "Splitting the rent",
  "A startup pitch",
  "A ceasefire",
];

export function ScenesVisual() {
  return (
    <ul aria-hidden className="flex flex-wrap gap-2">
      {SCENES.map((s, i) => (
        <li
          key={s}
          className={cn(
            "rounded-lg border px-3 py-2 text-sm",
            i % 3 === 0 ? "border-brand bg-brand text-white" : "border-line bg-background",
          )}
        >
          {s}
        </li>
      ))}
      <li className="inline-flex items-center gap-1 rounded-lg border border-dashed border-brand/50 px-3 py-2 text-sm text-brand">
        <PlusIcon weight="bold" className="size-3" />
        Describe your own
      </li>
    </ul>
  );
}

const STEPS = ["Listen", "Think privately", "Recall", "Speak"];

export function HarnessVisual() {
  return (
    <div aria-hidden>
      <div className="flex flex-wrap items-center gap-2">
        {STEPS.map((s, i) => (
          <Fragment key={s}>
            {i > 0 && <ArrowRightIcon className="size-3 text-muted-foreground" />}
            <span
              className={cn(
                "rounded-lg border px-3 py-2 font-mono text-xs",
                i === 1 ? "border-brand bg-brand/10 text-brand" : "border-line bg-background",
              )}
            >
              {s}
            </span>
          </Fragment>
        ))}
      </div>
      <p className="label-mono mt-3 inline-flex items-center gap-1">
        <ArrowUUpLeftIcon className="size-3" />
        Loop until confident
      </p>
    </div>
  );
}

const LOG: [string, string, boolean?][] = [
  ["Message 12", "Proposes a later handover", false],
  ["Private note", "“They care more about speed than price.”", true],
  ["Cost so far", "1,842 tokens", false],
  ["Rerun", "Same scene, new financial report", false],
];

export function RecordVisual() {
  return (
    <ol aria-hidden className="relative flex flex-col gap-3 border-l border-line pl-4">
      {LOG.map(([k, v, secret]) => (
        <li key={k} className="relative">
          <span className="absolute top-1.5 -left-[21px] size-2 rounded-full border border-brand bg-background" />
          <p className="label-mono inline-flex items-center gap-1">
            {secret && <LockSimpleIcon weight="bold" className="size-3" />}
            {k}
          </p>
          <p className="text-sm">{v}</p>
        </li>
      ))}
    </ol>
  );
}

const BRIEFING: [string, string][] = [
  ["Agreed", "Price and handover date"],
  ["Still open", "Who covers the warranty"],
  ["They cared about", "Closing before the month ends"],
  ["Next step", "Meet in person on Thursday"],
];

export function BriefingVisual() {
  return (
    <div aria-hidden className="rounded-lg border border-line bg-background p-4">
      <p className="label-mono text-brand">Your private briefing</p>
      <dl className="mt-3 flex flex-col">
        {BRIEFING.map(([k, v], i) => (
          <div key={k} className={cn("flex justify-between gap-4 py-2 text-sm", i > 0 && "border-t border-line")}>
            <dt className="text-muted-foreground">{k}</dt>
            <dd className="text-right">{v}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
