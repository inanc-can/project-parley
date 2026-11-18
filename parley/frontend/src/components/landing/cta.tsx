import { ArrowRightIcon } from "@phosphor-icons/react/dist/ssr";
import { cn } from "cn";
import Link from "next/link";

import { SITE_ONLY } from "@/lib/site";
import { TRANSITION } from "./motion";

export const FOCUS =
  "outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand";

/** The page's one primary action. The same label and target everywhere it appears. */
export function StartRoomButton({
  size = "base",
  inverse = false,
  className,
}: {
  size?: "base" | "sm";
  inverse?: boolean;
  className?: string;
}) {
  if (SITE_ONLY) {
    return (
      <span
        className={cn(
          "inline-flex items-center gap-2 rounded-lg px-3 py-2 font-semibold",
          inverse ? "bg-white/15 text-white" : "bg-secondary text-muted-foreground",
          size === "base" ? "text-base" : "text-sm",
          className,
        )}
      >
        Coming soon
      </span>
    );
  }
  return (
    <Link
      href="/start"
      className={cn(
        "group inline-flex items-center gap-2 rounded-lg px-3 py-2 font-semibold",
        inverse
          ? "bg-white text-brand hover:bg-secondary focus-visible:outline-white"
          : "bg-foreground text-background hover:bg-brand",
        "hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98]",
        size === "base" ? "text-base" : "text-sm",
        TRANSITION,
        FOCUS,
        className,
      )}
    >
      Start a room
      <ArrowRightIcon
        aria-hidden
        weight="bold"
        className={cn("size-4 group-hover:translate-x-0.5", TRANSITION)}
      />
    </Link>
  );
}

export const RISK_REVERSAL = "No signup. Your friend installs nothing. Your room stays at its link.";
