import type { ReactNode } from "react";

/** Plain reading layout for the legal pages. */
export function Prose({ title, updated, children }: { title: string; updated: string; children: ReactNode }) {
  return (
    <article className="mx-auto max-w-[680px] px-4 pt-40 pb-24">
      <p className="label-mono text-brand">Last updated {updated}</p>
      <h1 className="display-title mt-4 text-5xl">{title}</h1>
      <div className="mt-12 flex flex-col gap-6 text-base text-muted-foreground [&_h2]:display-title [&_h2]:mt-6 [&_h2]:text-2xl [&_h2]:text-foreground">
        {children}
      </div>
    </article>
  );
}
