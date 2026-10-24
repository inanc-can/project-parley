import Link from "next/link";

import { FOCUS, StartRoomButton } from "@/components/landing/cta";

export default function NotFound() {
  return (
    <main className="site-root flex flex-1 flex-col items-center justify-center px-4 py-24 text-center">
      <p className="label-mono text-brand">404 · No agreement reached</p>
      <h1 className="display-title mt-6 max-w-[680px] text-5xl md:text-6xl">
        No deal here.
        <br />
        This page doesn&apos;t exist.
      </h1>
      <p className="mt-6 max-w-[520px] text-lg text-muted-foreground">
        The link may be mistyped, or the room it pointed to was removed by its host.
      </p>
      <div className="mt-8 flex flex-col items-center gap-4">
        <StartRoomButton />
        <Link href="/" className={`rounded-sm text-sm text-muted-foreground hover:text-brand ${FOCUS}`}>
          Back to the home page
        </Link>
      </div>
    </main>
  );
}
