import type { Metadata } from "next";

import { Prose } from "@/components/landing/prose";

export const metadata: Metadata = {
  title: "Terms",
  description: "The ground rules for using Parley.",
};

export default function Terms() {
  return (
    <Prose title="Terms" updated="18 October 2026">
      <p>
        Parley is research software provided as is, without warranty. By using a Parley
        instance you agree to the points below.
      </p>
      <h2>Your content</h2>
      <p>
        You are responsible for the games and strategies you write. Don&apos;t put personal,
        confidential or harmful material into a room: it is sent to an AI model provider.
      </p>
      <h2>AI output</h2>
      <p>
        Agents and the judge are language models. They make mistakes, break rules and sometimes
        say things that are wrong. Treat transcripts and scores as experimental results, not
        advice.
      </p>
      <h2>Costs</h2>
      <p>
        The host pays their AI provider for the matches run on their instance and decides which
        models are available.
      </p>
      <h2>Changes</h2>
      <p>These terms may change. The date at the top shows the latest version.</p>
    </Prose>
  );
}
