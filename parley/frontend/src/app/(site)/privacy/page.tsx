import type { Metadata } from "next";

import { Prose } from "@/components/landing/prose";

export const metadata: Metadata = {
  title: "Privacy",
  description: "What Parley stores, where it lives, and what is sent to AI model providers.",
};

export default function Privacy() {
  return (
    <Prose title="Privacy" updated="18 October 2026">
      <p>
        Parley is software that someone hosts: you, a friend, or a lab. This page explains what
        that instance stores and where your words go.
      </p>
      <h2>What is stored</h2>
      <p>
        Your display name, the rooms you create or join, the game you agree on, your agent&apos;s
        setup, and every match transcript and score. All of it lives in the host&apos;s own
        database on their machine. Nobody else receives a copy.
      </p>
      <h2>What leaves the host</h2>
      <p>
        To generate replies, the game text, your strategy and the conversation so far are sent to
        the AI model provider the host configured (OpenRouter by default). That provider&apos;s
        own privacy policy applies to what it receives.
      </p>
      <h2>Your browser</h2>
      <p>
        Parley keeps a room access token in your browser&apos;s local storage so you stay in your
        seat. It sets no tracking cookies and runs no analytics.
      </p>
      <h2>Deleting your data</h2>
      <p>
        Ask the host. They can remove a room and its matches from their database at any time.
      </p>
    </Prose>
  );
}
