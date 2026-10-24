import type { ReactNode } from "react";

import { Reveal } from "./reveal";

/** Editorial section opener: a hairline, a numbered mono label, a serif title. */
export function SectionHead({
  index,
  label,
  id,
  title,
  children,
}: {
  index: string;
  label: string;
  id: string;
  title: ReactNode;
  children?: ReactNode;
}) {
  return (
    <Reveal>
      <div className="flex items-center gap-3 border-t border-line pt-4">
        <span className="label-mono text-brand">{index}</span>
        <span className="label-mono">{label}</span>
      </div>
      <h2 id={id} className="display-title mt-6 max-w-[760px] text-4xl md:text-5xl">
        {title}
      </h2>
      {children && <p className="mt-6 max-w-[620px] text-lg text-muted-foreground">{children}</p>}
    </Reveal>
  );
}
