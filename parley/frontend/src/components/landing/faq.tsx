import { PlusIcon } from "@phosphor-icons/react/dist/ssr";
import { cn } from "cn";

import { FOCUS } from "./cta";
import { TRANSITION } from "./motion";

export type QA = { q: string; a: string };

/** Native disclosure rows between hairlines: keyboard and screen reader support for free. */
export function Faq({ items }: { items: QA[] }) {
  return (
    <div className="border-b border-line">
      {items.map((it) => (
        <details key={it.q} className="group border-t border-line">
          <summary
            className={cn(
              "flex cursor-pointer list-none items-center justify-between gap-6 rounded-sm py-6 text-lg font-medium hover:text-brand [&::-webkit-details-marker]:hidden",
              TRANSITION,
              FOCUS,
            )}
          >
            {it.q}
            <span className="flex size-8 shrink-0 items-center justify-center rounded-full border border-line text-brand group-open:bg-brand group-open:text-white">
              <PlusIcon aria-hidden weight="bold" className={cn("size-3 group-open:rotate-45", TRANSITION)} />
            </span>
          </summary>
          <p className="max-w-[620px] pb-6 text-base text-muted-foreground">{it.a}</p>
        </details>
      ))}
    </div>
  );
}
