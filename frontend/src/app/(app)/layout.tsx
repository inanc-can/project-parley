import type { Metadata } from "next";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";

// Rooms are private links: keep the app out of search results.
export const metadata: Metadata = { robots: { index: false } };

export default function AppLayout({ children }: LayoutProps<"/">) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="sticky top-0 z-10 flex h-14 shrink-0 items-center gap-2 border-b border-line bg-background/95 px-3 backdrop-blur-sm">
          <SidebarTrigger className="text-muted-foreground" />
          <span className="display-title text-lg md:hidden">Parley</span>
        </header>
        {children}
      </SidebarInset>
    </SidebarProvider>
  );
}
