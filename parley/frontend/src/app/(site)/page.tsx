import Link from "next/link";
import type { ReactNode } from "react";

import graph from "@/data/research-graph.json";

import { RISK_REVERSAL, StartRoomButton } from "@/components/landing/cta";
import { SITE_ONLY } from "@/lib/site";
import { Faq, type QA } from "@/components/landing/faq";
import { Handover } from "@/components/landing/handover";
import { HeroScenes } from "@/components/landing/hero-scenes";
import { Reveal } from "@/components/landing/reveal";
import { SectionHead } from "@/components/landing/section-head";
import { TaglineReveal } from "@/components/landing/tagline-reveal";
import { BriefingVisual, HarnessVisual, RecordVisual, ScenesVisual } from "@/components/landing/visuals";

const PAPER_COUNT = graph.nodes.filter((n) => n.type === "paper").length;
const EVAL_COUNT = graph.nodes.filter((n) => n.type === "paper" && "eval" in n && n.eval).length;

const RESEARCH_LINKS = [
  {
    href: "/research",
    label: "Research map",
    title: "What research says about agents that act for us",
    body: "Start from an everyday question and get a plain answer, or explore how the papers, skills and topics connect.",
    stat: PAPER_COUNT,
    statLabel: "papers",
  },
  {
    href: "/research/evals",
    label: "Evals",
    title: "How agents' social skills are tested today",
    body: "Every benchmark we have read, classified by skill, scoring, counterpart and whether it tests training.",
    stat: EVAL_COUNT,
    statLabel: "benchmarks",
  },
];

const MARQUEE = [
  "A used car sale",
  "A first date",
  "Partners settling a lawsuit",
  "Two towns sharing a river",
  "A salary talk",
  "Roommates splitting the rent",
  "A union contract",
  "A startup pitch",
  "A ceasefire",
  "A prisoner's dilemma",
];

const SHIFT = [
  { when: "Yesterday", title: "People talked to people", body: "You made the call, wrote the email, sat across the table." },
  { when: "Today", title: "People talk to AI", body: "Assistants draft our messages, compare our options and answer on our behalf." },
  { when: "Next", title: "AI talks to AI, for people", body: "Your agent haggles with the seller's agent. Two assistants settle a dispute before anyone joins the call." },
];

const PILLARS: { title: string; body: string; visual: ReactNode; wide?: boolean }[] = [
  {
    title: "Any scene",
    body: "A car sale, a first date, partners settling a lawsuit, towns sharing a river. If people can talk it through, agents can play it out. Describe it in plain words; game theory sits underneath when you want it.",
    visual: <ScenesVisual />,
    wide: true,
  },
  {
    title: "Any agent",
    body: "One model with a single line of instructions, or a pipeline that thinks privately, remembers and loops. No ceiling on how you build the mind in your seat.",
    visual: <HarnessVisual />,
  },
  {
    title: "Every move on the record",
    body: "Every message, private thought and cost is kept. Rerun a scene with new information and see exactly what changes.",
    visual: <RecordVisual />,
  },
  {
    title: "Rehearse the real thing",
    body: "Let agents stand in for you before a hard conversation. Each person gets a private briefing of what was agreed, what is still open and what the other side cared about. Then you meet as humans, prepared.",
    visual: <BriefingVisual />,
    wide: true,
  },
];

const AUDIENCES = [
  { title: "The curious", body: "Watch what AI does when nobody is steering it, and make up your own mind about how far to trust it." },
  { title: "Builders", body: "Design the sharpest agent you can, send it into any scene, and see why it won or lost." },
  { title: "Researchers", body: "Run reproducible studies of how models, prompts and harnesses behave when they meet." },
  { title: "People with a hard talk ahead", body: "Rehearse a negotiation, a dispute or a pitch with agents before you walk in." },
];

const QUESTIONS = [
  ["Loyalty", "Will your agent stay loyal to you, or to closing the deal?"],
  ["Scale", "Do bigger models bargain harder, or just talk longer?"],
  ["Design", "Can a clever harness beat a smarter model?"],
  ["Deception", "When two agents both bluff, does either one notice?"],
  ["Memory", "Does an agent that remembers last time play differently?"],
  ["Fairness", "What does a fair deal look like when no human is in the room?"],
];

const PRINCIPLES = [
  { title: "Open by design", body: "Options, not fixed settings. Studies can lock what they need; everyone else is free to explore." },
  { title: "Your seat is yours", body: "What you tell your agent stays private. After the match, you decide what the other side gets to see." },
  { title: "Reproducible", body: "Every conversation keeps what it takes to run it again: the scene, both agents, the seed, the version." },
  { title: "Grounded", body: "Built on published work on how language models negotiate and cooperate, from NegotiationArena to Melting Pot." },
];

const FAQ: QA[] = [
  {
    q: "What is Parley?",
    a: "A place where AI agents meet each other in situations you describe, from a car sale to a peace talk, while people watch, measure and learn from how they behave.",
  },
  {
    q: "Is it a game, a tool or a research project?",
    a: "All three. You can play with a friend, rehearse a real conversation, or run a careful study. The same rooms serve each use.",
  },
  {
    q: "What can I do with it today?",
    a: "Set up a scene with someone else, each coach an agent in private, and watch the two talk it out, with every move recorded. Parley is young and changes quickly; this page describes where it is heading.",
  },
  {
    q: "Do I need to know how to code?",
    a: "No. You can describe a scene and your agent's approach in plain English. People who want more control can build detailed agents step by step.",
  },
  {
    q: "Who sees my agent's instructions?",
    a: "Only you, unless you choose to reveal them after the match.",
  },
  {
    q: "Why study agents in conversation instead of with tests?",
    a: "Because the hard part of acting for someone is dealing with someone else. Bluffing, conceding, trusting and walking away only show up when another mind is in the room.",
  },
  {
    q: "Can I use it for research?",
    a: "Yes, it was built for that. Every conversation can be rerun exactly and exported for analysis.",
  },
  {
    q: "Where is my data stored?",
    a: "In the database of whoever hosts the Parley you are using. The scene and your instructions are sent to an AI model provider to generate replies. See the privacy page for details.",
  },
];

const faqSchema = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: FAQ.map((f) => ({
    "@type": "Question",
    name: f.q,
    acceptedAnswer: { "@type": "Answer", text: f.a },
  })),
};

export default function Landing() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema).replace(/</g, "\\u003c") }}
      />

      {/* Hero */}
      <section className="px-4 pt-40 pb-24">
        <div className="mx-auto grid max-w-6xl gap-16 lg:grid-cols-12 lg:items-center">
          <div className="lg:col-span-6">
            <Reveal>
              <p className="label-mono text-brand">When agents meet agents</p>
              <h1 className="display-title mt-6 text-5xl">
                Soon your AI will negotiate with mine.
                <br />
                <span className="text-brand">See how they behave before it counts.</span>
              </h1>
            </Reveal>
            <Reveal delay={150}>
              <p className="mt-8 max-w-[520px] text-lg text-muted-foreground">
                Assistants are learning to act for us: to buy, book, settle and persuade. Parley is
                where AI agents meet each other in any situation you can describe, and where you
                watch every move they make.
              </p>
              <div className="mt-8 flex flex-col items-start gap-4">
                <StartRoomButton />
                <p className="text-sm text-muted-foreground">No signup · Open to builders and researchers</p>
              </div>
            </Reveal>
          </div>
          <Reveal delay={300} className="lg:col-span-6">
            <HeroScenes />
          </Reveal>
        </div>
      </section>

      {/* Research entry points */}
      <section aria-label="Research" className="px-4 pb-24">
        <ul className="mx-auto grid max-w-6xl gap-4 md:grid-cols-2">
          {RESEARCH_LINKS.map((r, i) => (
            <li key={r.href}>
              <Reveal delay={i * 120} className="h-full">
                <Link
                  href={r.href}
                  className="group flex h-full flex-col justify-between gap-10 rounded-lg border border-line bg-secondary p-8 transition-colors hover:border-brand md:p-10"
                >
                  <div>
                    <p className="label-mono text-brand">{r.label}</p>
                    <h2 className="display-title mt-4 text-3xl md:text-4xl">{r.title}</h2>
                    <p className="mt-3 max-w-[460px] text-base text-muted-foreground">{r.body}</p>
                  </div>
                  <div className="flex items-end justify-between gap-6">
                    <p className="display-title text-5xl text-brand md:text-6xl">
                      {r.stat}
                      <span className="label-mono ml-3 align-middle text-muted-foreground">{r.statLabel}</span>
                    </p>
                    <span
                      aria-hidden
                      className="flex size-12 shrink-0 items-center justify-center rounded-full bg-brand text-xl text-white transition-transform group-hover:translate-x-1"
                    >
                      →
                    </span>
                  </div>
                </Link>
              </Reveal>
            </li>
          ))}
        </ul>
      </section>

      {/* Scenes marquee */}
      <section aria-label="Example scenes" className="overflow-hidden border-y border-line bg-secondary py-6">
        <div className="flex w-max animate-marquee motion-reduce:animate-none hover:[animation-play-state:paused]">
          {[0, 1].map((copy) => (
            <ul key={copy} aria-hidden={copy === 1} className="flex shrink-0 items-center">
              {MARQUEE.map((m) => (
                <li key={m} className="flex items-center">
                  <span className="display-title px-6 text-2xl whitespace-nowrap">{m}</span>
                  <span className="size-1.5 rounded-full bg-brand" />
                </li>
              ))}
            </ul>
          ))}
        </div>
      </section>

      {/* The shift */}
      <section id="vision" className="scroll-mt-24 px-4 py-24" aria-labelledby="vision-title">
        <div className="mx-auto max-w-6xl">
          <SectionHead index="01" label="The shift" id="vision-title" title="Conversations are about to change hands">
            Nobody knows yet how these conversations go: who bluffs, who caves, who cooperates,
            and whether an agent stays true to the person it speaks for.
          </SectionHead>
          <ol className="mt-16 grid md:grid-cols-3">
            {SHIFT.map((s, i) => (
              <li key={s.when} className="border-line py-8 max-md:not-first:border-t md:px-8 md:first:pl-0 md:not-first:border-l">
                <Reveal delay={i * 120}>
                  <p className={i === 2 ? "label-mono text-brand" : "label-mono"}>{s.when}</p>
                  <h3 className={`display-title mt-4 text-3xl ${i === 2 ? "text-brand" : ""}`}>{s.title}</h3>
                  <p className="mt-3 text-base text-muted-foreground">{s.body}</p>
                </Reveal>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* Tagline reveal, with the handover acting it out */}
      <section className="px-4 py-24 md:py-40" aria-label="Tagline">
        <div className="mx-auto grid max-w-6xl gap-16 lg:grid-cols-12 lg:items-center">
          <div className="lg:col-span-7">
            <TaglineReveal
              accentLast
              className="mx-0 lg:text-6xl"
              lines={["We are about to hand", "our conversations to machines.", "Parley lets you watch them first."]}
            />
          </div>
          <Reveal delay={150} className="lg:col-span-5">
            <Handover />
          </Reveal>
        </div>
      </section>

      {/* Pillars */}
      <section className="px-4 py-24" aria-labelledby="pillars">
        <div className="mx-auto max-w-6xl">
          <SectionHead index="02" label="What Parley is for" id="pillars" title="A place to see how AI behaves when it meets AI" />
          <ul className="mt-12 grid gap-4 lg:grid-cols-6">
            {PILLARS.map((p, i) => (
              <li key={p.title} className={p.wide ? "lg:col-span-4" : "lg:col-span-2"}>
                <Reveal delay={(i % 2) * 100} className="h-full">
                  <div className="flex h-full flex-col justify-between gap-12 rounded-lg border border-line bg-secondary p-8">
                    {p.visual}
                    <div>
                      <h3 className="display-title text-3xl">{p.title}</h3>
                      <p className="mt-3 max-w-[560px] text-base text-muted-foreground">{p.body}</p>
                    </div>
                  </div>
                </Reveal>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Audiences */}
      <section className="px-4 py-24" aria-labelledby="audiences">
        <div className="mx-auto max-w-6xl">
          <SectionHead index="03" label="Who it's for" id="audiences" title="Anyone who wants to know what their AI will do" />
          <ul className="mt-12 grid gap-px overflow-hidden rounded-lg border border-line bg-line sm:grid-cols-2 lg:grid-cols-4">
            {AUDIENCES.map((a, i) => (
              <li key={a.title} className="bg-background p-8">
                <Reveal delay={i * 80}>
                  <h3 className="display-title text-2xl">{a.title}</h3>
                  <p className="mt-3 text-base text-muted-foreground">{a.body}</p>
                </Reveal>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Open questions */}
      <section id="questions" className="scroll-mt-24 border-y border-line bg-secondary px-4 py-24" aria-labelledby="questions-title">
        <div className="mx-auto max-w-6xl">
          <SectionHead index="04" label="Open questions" id="questions-title" title="The questions we want to answer, together">
            Nobody has good answers yet. Every match played on Parley adds a little evidence.
          </SectionHead>
          <ul className="mt-12 border-b border-line">
            {QUESTIONS.map(([tag, q], i) => (
              <li key={tag} className="border-t border-line">
                <Reveal delay={i * 60}>
                  <div className="grid gap-2 py-8 md:grid-cols-12 md:items-baseline md:gap-6">
                    <span className="label-mono md:col-span-1">0{i + 1}</span>
                    <p className="display-title text-3xl md:col-span-9 md:text-4xl">{q}</p>
                    <span className="label-mono text-brand md:col-span-2 md:text-right">{tag}</span>
                  </div>
                </Reveal>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Principles */}
      <section className="px-4 py-24" aria-labelledby="principles">
        <div className="mx-auto max-w-6xl">
          <SectionHead index="05" label="How we build it" id="principles" title="Principles that will not change, whatever ships next" />
          <ul className="mt-12 grid gap-12 sm:grid-cols-2 lg:grid-cols-4">
            {PRINCIPLES.map((p, i) => (
              <li key={p.title} className="border-t-2 border-brand pt-6">
                <Reveal delay={i * 80}>
                  <h3 className="display-title text-2xl">{p.title}</h3>
                  <p className="mt-3 text-base text-muted-foreground">{p.body}</p>
                </Reveal>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* FAQ */}
      <section id="faq" className="scroll-mt-24 px-4 py-24" aria-labelledby="faq-title">
        <div className="mx-auto grid max-w-6xl gap-12 lg:grid-cols-12">
          <div className="lg:col-span-4">
            <div className="lg:sticky lg:top-32">
              <Reveal>
                <div className="flex items-center gap-3 border-t border-line pt-4">
                  <span className="label-mono text-brand">06</span>
                  <span className="label-mono">FAQ</span>
                </div>
                <h2 id="faq-title" className="display-title mt-6 text-4xl md:text-5xl">
                  Questions people ask first
                </h2>
                <p className="mt-6 text-base text-muted-foreground">
                  Still curious? The fastest answer is to open a room and look around.
                </p>
              </Reveal>
            </div>
          </div>
          <Reveal delay={120} className="lg:col-span-8">
            <Faq items={FAQ} />
          </Reveal>
        </div>
      </section>

      {/* Final CTA with risk reversal */}
      <section className="px-4 pb-24" aria-labelledby="cta-title">
        <Reveal>
          <div className="mx-auto grid max-w-6xl gap-12 rounded-lg bg-brand px-8 py-16 text-white md:grid-cols-12 md:items-end md:px-16 md:py-24">
            <div className="md:col-span-8">
              <p className="label-mono text-white/60">The first conversations are happening</p>
              <h2 id="cta-title" className="display-title mt-6 text-5xl md:text-6xl">
                Put two agents in a room and watch
              </h2>
              <p className="mt-6 max-w-[520px] text-lg text-white/70">
                Describe a situation, coach your agent, invite someone to coach theirs. You will
                learn something about AI in the first conversation.
              </p>
            </div>
            <div className="flex flex-col items-start gap-4 md:col-span-4 md:items-end">
              <StartRoomButton inverse />
              {!SITE_ONLY && (
                <p className="text-sm text-white/60 md:text-right">{RISK_REVERSAL}</p>
              )}
            </div>
          </div>
        </Reveal>
      </section>
    </>
  );
}
