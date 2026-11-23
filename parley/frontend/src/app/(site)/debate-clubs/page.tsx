import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

import { Reveal } from "@/components/landing/reveal";

export const metadata: Metadata = {
  title: "AI Debate Clubs",
  description:
    "A club night where debaters argue with, coach and judge AI debaters, and their decisions help research on how people oversee AI.",
};

const SIDES = [
  { title: "Your club brings", items: ["Debaters", "Trained judges", "Motions and formats", "An audience"] },
  {
    title: "Parley brings",
    items: ["A working platform for AI debates", "The technical setup on the night", "A link to research on AI oversight"],
  },
  {
    title: "Your club gets",
    items: ["A new event format that draws members", "Members who can work with AI and judge it", "Credit in any research that comes out of it"],
  },
];

const FORMATS = [
  { title: "Human vs AI", body: "Members debate an AI team on a motion, judged by a human panel." },
  {
    title: "Coach the bot",
    body: "Teams brief the same AI model with a strategy; the panel ranks the rounds and an AI judge runs alongside for comparison.",
  },
  {
    title: "Judge the AI",
    body: "Members adjudicate AI rounds with written reasons, then compare their calls with an experienced panel.",
  },
];

export default function DebateClubsPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 pt-32 pb-24">
      <Reveal>
        <div className="flex items-center gap-3 border-t border-line pt-4">
          <span className="label-mono text-brand">Collaborate</span>
          <span className="label-mono">AI Debate Clubs</span>
        </div>
        <h1 className="display-title mt-6 max-w-[820px] text-4xl md:text-6xl">
          Debaters are the people best trained to judge an argument. AI needs that judgment.
        </h1>
        <p className="mt-6 max-w-[640px] text-lg text-muted-foreground">
          As far as we could find, no club runs AI debate as a regular series. We want to start one
          with debate clubs: a night where members argue with, coach and judge AI debaters, and what
          they decide helps research on how people oversee AI.
        </p>
        <div className="mt-10 flex max-w-[640px] items-center gap-5 rounded-lg border border-line bg-secondary p-5">
          {/* Logo from debattierclub-muenchen.de; confirm the club is happy with its use. */}
          <Image
            src="/partners/debattierclub-muenchen.png"
            alt="Debattierclub München logo"
            width={72}
            height={72}
            className="size-[72px] shrink-0"
          />
          <div>
            <p className="label-mono text-brand">Pilot in discussion</p>
            <p className="mt-1 text-base">
              A first pilot evening is being discussed with Debattierclub München e.V.
            </p>
          </div>
        </div>
      </Reveal>

      <section aria-labelledby="sides" className="mt-20">
        <div className="flex items-center gap-3 border-t border-line pt-4">
          <span className="label-mono text-brand">01</span>
          <span id="sides" className="label-mono">What each side brings</span>
        </div>
        <ul className="mt-8 grid gap-px overflow-hidden rounded-lg border border-line bg-line md:grid-cols-3">
          {SIDES.map((s, i) => (
            <li key={s.title} className="bg-background p-8">
              <Reveal delay={i * 100}>
                <h2 className="display-title text-2xl">{s.title}</h2>
                <ul className="mt-4 space-y-2 text-base text-muted-foreground">
                  {s.items.map((item) => (
                    <li key={item} className="flex gap-3">
                      <span className="mt-2.5 size-1.5 shrink-0 rounded-full bg-brand" />
                      {item}
                    </li>
                  ))}
                </ul>
              </Reveal>
            </li>
          ))}
        </ul>
      </section>

      <section aria-labelledby="formats" className="mt-20">
        <div className="flex items-center gap-3 border-t border-line pt-4">
          <span className="label-mono text-brand">02</span>
          <span id="formats" className="label-mono">Formats</span>
        </div>
        <h2 className="display-title mt-6 max-w-[760px] text-3xl md:text-4xl">
          People never stand aside: they speak or they decide.
        </h2>
        <ul className="mt-10 grid gap-8 md:grid-cols-3">
          {FORMATS.map((f, i) => (
            <li key={f.title} className="border-t-2 border-brand pt-6">
              <Reveal delay={i * 100}>
                <h3 className="display-title text-2xl">{f.title}</h3>
                <p className="mt-3 text-base text-muted-foreground">{f.body}</p>
              </Reveal>
            </li>
          ))}
        </ul>
      </section>

      <p className="mt-20 text-sm text-muted-foreground">
        Curious what research says about AI that argues for people?{" "}
        <Link href="/research" className="text-brand underline-offset-4 hover:underline">
          Explore the research map
        </Link>
      </p>
    </div>
  );
}
