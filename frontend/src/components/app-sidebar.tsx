"use client";

import { Bot, DoorOpen, Gamepad2, Network, Plus, Swords, Trophy, type LucideIcon } from "lucide-react";
import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { Suspense, useEffect, type MouseEvent } from "react";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuBadge,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  useSidebar,
} from "@/components/ui/sidebar";
import {
  type RoomSummary,
  type RoomTab,
  loadRoomSummary,
  parseTab,
  setRoomTab,
  useKnownRooms,
  useRoomSummaries,
} from "@/lib/room-store";

// Editorial touches on top of the shadcn defaults: mono group labels, a navy rule on the active item.
const GROUP_LABEL = "label-mono h-7 text-[0.68rem] text-muted-foreground";
const ITEM = "data-active:font-medium data-active:shadow-[inset_2px_0_0_var(--brand)]";

const STEPS: { tab: RoomTab; label: string; icon: LucideIcon; marker: (r: RoomSummary) => string }[] = [
  { tab: "map", label: "Map", icon: Network, marker: () => "" },
  { tab: "game", label: "Game", icon: Gamepad2, marker: (r) => (r.locked ? "✓" : "") },
  { tab: "seat", label: "My agent", icon: Bot, marker: (r) => (r.ready ? "✓" : "") },
  { tab: "match", label: "Match", icon: Swords, marker: (r) => (r.running ? "●" : "") },
  { tab: "results", label: "Results", icon: Trophy, marker: () => "" },
];

export function AppSidebar() {
  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="h-14 justify-center border-b border-sidebar-border">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Parley"
              className="hover:bg-transparent active:bg-transparent"
              render={<Link href="/" />}
            >
              {/* Monogram on the icon rail, wordmark otherwise. */}
              <span className="display-title hidden size-4 shrink-0 items-center justify-center text-lg text-brand group-data-[collapsible=icon]:flex">
                P
              </span>
              <span className="display-title text-xl group-data-[collapsible=icon]:hidden">Parley</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        {/* Everything below reads the URL or localStorage, so it renders on the client only. */}
        <Suspense fallback={<NewRoomGroup active={false} />}>
          <SidebarNav />
        </Suspense>
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  );
}

function useCloseOnMobile() {
  const { isMobile, setOpenMobile } = useSidebar();
  return () => {
    if (isMobile) setOpenMobile(false);
  };
}

function NewRoomGroup({ active }: { active: boolean }) {
  const close = useCloseOnMobile();
  return (
    <SidebarGroup>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton
            isActive={active}
            tooltip="New room"
            className={ITEM}
            render={<Link href="/" onClick={close} />}
          >
            <Plus />
            <span>New room</span>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarGroup>
  );
}

function SidebarNav() {
  const pathname = usePathname();
  const roomId = /^\/room\/([^/]+)/.exec(pathname)?.[1] ?? null;
  const summaries = useRoomSummaries();

  return (
    <>
      <NewRoomGroup active={pathname === "/"} />
      {roomId && <RoomSteps roomId={roomId} summary={summaries.get(roomId)} />}
      <YourRooms activeId={roomId} summaries={summaries} />
    </>
  );
}

function RoomSteps({ roomId, summary }: { roomId: string; summary: RoomSummary | undefined }) {
  const tab = parseTab(useSearchParams().get("tab"));
  const close = useCloseOnMobile();

  function go(e: MouseEvent, next: RoomTab) {
    // Let modified clicks open a new tab; otherwise switch in place without a navigation.
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    e.preventDefault();
    setRoomTab(next);
    close();
  }

  return (
    <SidebarGroup>
      <SidebarGroupLabel className={GROUP_LABEL}>This room</SidebarGroupLabel>
      <SidebarGroupContent>
        <SidebarMenu>
          {STEPS.map((s) => {
            const marker = summary ? s.marker(summary) : "";
            return (
              <SidebarMenuItem key={s.tab}>
                <SidebarMenuButton
                  isActive={tab === s.tab}
                  tooltip={marker ? `${s.label} ${marker}` : s.label}
                  className={ITEM}
                  render={<a href={`/room/${roomId}?tab=${s.tab}`} onClick={(e) => go(e, s.tab)} />}
                >
                  <s.icon />
                  <span>{s.label}</span>
                </SidebarMenuButton>
                {marker && (
                  <SidebarMenuBadge className={marker === "●" ? "text-brand" : "text-muted-foreground"}>
                    {marker}
                  </SidebarMenuBadge>
                )}
              </SidebarMenuItem>
            );
          })}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  );
}

function YourRooms({
  activeId,
  summaries,
}: {
  activeId: string | null;
  summaries: ReadonlyMap<string, RoomSummary>;
}) {
  const rooms = useKnownRooms();
  const close = useCloseOnMobile();

  useEffect(() => {
    for (const id of rooms) loadRoomSummary(id);
  }, [rooms]);

  return (
    <SidebarGroup>
      <SidebarGroupLabel className={GROUP_LABEL}>Your rooms</SidebarGroupLabel>
      <SidebarGroupContent>
        {rooms.length === 0 ? (
          <p className="px-2 py-1 text-xs text-muted-foreground group-data-[collapsible=icon]:hidden">
            Rooms you create or join show up here.
          </p>
        ) : (
          <SidebarMenu>
            {rooms.map((id) => {
              const title = summaries.get(id)?.title;
              return (
                <SidebarMenuItem key={id}>
                  <SidebarMenuButton
                    isActive={id === activeId}
                    tooltip={title ? `${title} · ${id}` : id}
                    className={`${ITEM} pr-16`}
                    render={<Link href={`/room/${id}`} onClick={close} />}
                  >
                    <DoorOpen />
                    <span>{title || id}</span>
                  </SidebarMenuButton>
                  {title && (
                    <SidebarMenuBadge className="font-mono text-[0.65rem] font-normal text-muted-foreground">
                      {id}
                    </SidebarMenuBadge>
                  )}
                </SidebarMenuItem>
              );
            })}
          </SidebarMenu>
        )}
      </SidebarGroupContent>
    </SidebarGroup>
  );
}
