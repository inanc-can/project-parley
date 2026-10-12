import { Suspense } from "react";

import { RoomClient } from "@/components/room/room-client";

// Route params are runtime data under cacheComponents, so the client part sits in Suspense.
export default function RoomPage() {
  return (
    <Suspense fallback={<p className="text-muted-foreground p-8">Loading room…</p>}>
      <RoomClient />
    </Suspense>
  );
}
