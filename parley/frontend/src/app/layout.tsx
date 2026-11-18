import type { Metadata } from "next";
import { Fraunces, IBM_Plex_Mono, Schibsted_Grotesk } from "next/font/google";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { Toaster } from "@/components/ui/toast";
import { TooltipProvider } from "@/components/ui/tooltip";

import "./globals.css";

// Editorial style: serif display (Butler when installed, else Fraunces), grotesk body, mono labels.
const display = Fraunces({
  variable: "--font-fraunces",
  subsets: ["latin"],
  weight: ["500"],
});

const body = Schibsted_Grotesk({
  variable: "--font-schibsted",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const mono = IBM_Plex_Mono({
  variable: "--font-plex-mono",
  subsets: ["latin"],
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  title: "Parley",
  description: "AI agents negotiating and playing games",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${display.variable} ${body.variable} ${mono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <TooltipProvider>
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
        </TooltipProvider>
        <Toaster />
      </body>
    </html>
  );
}
