"use client";

import { FileText, Globe, Paperclip, Sparkles, X } from "lucide-react";
import { useRef, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { api } from "@/lib/api";
import { notifyError, notifyInfo } from "@/lib/notify";
import type { SharedFile } from "@/lib/types";

// Anything a chat box would take; the server converts it to text (images get a description).
const ACCEPT =
  ".pdf,.docx,.pptx,.xlsx,.xls,.csv,.tsv,.txt,.md,.json,.xml,.html,.htm,.epub,.zip,.msg,.ipynb,image/*,text/*";

function readBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result).split(",", 2)[1] ?? "");
    reader.onerror = () => reject(reader.error ?? new Error(`couldn't read ${file.name}`));
    reader.readAsDataURL(file);
  });
}

// Converts each file on the server; the ones that fail are reported and skipped.
async function convert(roomId: string, files: File[]): Promise<SharedFile[]> {
  const results = await Promise.allSettled(
    files.map(async (f) => api.addFile(roomId, { name: f.name, mime: f.type, data: await readBase64(f) })),
  );
  results.forEach((r, i) => r.status === "rejected" && notifyError(r.reason, `Couldn't add ${files[i].name}`));
  return results.flatMap((r) => (r.status === "fulfilled" ? [r.value] : []));
}

const tokens = (text: string) => Math.max(1, Math.round(text.length / 4)).toLocaleString();

export function SharedFiles({
  roomId,
  files,
  context,
  disabled,
  onFiles,
  onContext,
}: {
  roomId: string;
  files: SharedFile[];
  context: string;
  disabled: boolean;
  onFiles: (files: SharedFile[]) => void;
  onContext: (text: string) => void;
}) {
  const attachInput = useRef<HTMLInputElement>(null);
  const summaryInput = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState<"attach" | "summary" | "research" | null>(null);
  const [researchOpen, setResearchOpen] = useState(false);
  const [topic, setTopic] = useState("");
  const [open, setOpen] = useState<string | null>(null); // sha256 of the file being previewed

  async function attach(list: File[]) {
    setBusy("attach");
    try {
      const added = await convert(roomId, list);
      if (added.length) onFiles([...files, ...added]);
    } finally {
      setBusy(null);
    }
  }

  async function summarise(list: File[]) {
    setBusy("summary");
    try {
      const read = await convert(roomId, list);
      if (!read.length) return;
      const { text } = await api.summariseFiles(roomId, read, context);
      onContext(context.trim() ? `${context.trimEnd()}\n\n${text}` : text);
      notifyInfo("Summary added to the shared context", "Not saved yet. Review it, then press Save version.");
    } catch (e) {
      notifyError(e, "Couldn't summarise the files");
    } finally {
      setBusy(null);
    }
  }

  async function research() {
    if (!topic.trim()) return;
    setBusy("research");
    try {
      const { text } = await api.research(roomId, topic, context);
      onContext(context.trim() ? `${context.trimEnd()}\n\n${text}` : text);
      setResearchOpen(false);
      setTopic("");
      notifyInfo("Research added to the shared context", "Not saved yet. Check the facts and sources, then press Save version.");
    } catch (e) {
      notifyError(e, "Couldn't research that");
    } finally {
      setBusy(null);
    }
  }

  function picker(ref: React.RefObject<HTMLInputElement | null>, handle: (files: File[]) => void) {
    return (
      <input
        ref={ref}
        type="file"
        multiple
        accept={ACCEPT}
        className="hidden"
        onChange={(e) => {
          const list = Array.from(e.target.files ?? []);
          e.target.value = ""; // picking the same file again should work
          if (list.length) handle(list);
        }}
      />
    );
  }

  const shown = files.find((f) => f.sha256 === open);

  return (
    <div className="flex flex-col gap-2">
      {files.length > 0 && (
        <ul className="flex flex-wrap gap-2">
          {files.map((f, i) => (
            <li
              key={`${f.sha256}-${i}`}
              className="flex items-center gap-1.5 rounded-md border border-line bg-muted/40 py-1 pr-1 pl-2 text-sm"
            >
              <FileText className="size-3.5 shrink-0 text-muted-foreground" />
              <button
                type="button"
                className="max-w-56 truncate hover:underline"
                title="Show the text agents read"
                onClick={() => setOpen(open === f.sha256 ? null : f.sha256)}
              >
                {f.name}
              </button>
              <span className="label-mono text-[0.65rem] text-muted-foreground">~{tokens(f.text)} tokens</span>
              <Button
                type="button"
                variant="ghost"
                size="icon-xs"
                aria-label={`Remove ${f.name}`}
                disabled={disabled}
                onClick={() => {
                  onFiles(files.filter((_, j) => j !== i));
                  if (open === f.sha256) setOpen(null);
                }}
              >
                <X />
              </Button>
            </li>
          ))}
        </ul>
      )}
      {shown && (
        <pre className="max-h-64 overflow-auto rounded-md border border-line bg-muted/30 p-3 font-mono text-xs whitespace-pre-wrap">
          {shown.text}
        </pre>
      )}
      <div className="flex flex-wrap items-center gap-2">
        {picker(attachInput, attach)}
        {picker(summaryInput, summarise)}
        <Button
          type="button"
          variant="outline"
          size="sm"
          disabled={disabled || busy !== null}
          onClick={() => attachInput.current?.click()}
        >
          <Paperclip />
          {busy === "attach" ? "Reading files…" : "Attach files"}
        </Button>
        <Button
          type="button"
          variant="outline"
          size="sm"
          disabled={disabled || busy !== null}
          onClick={() => summaryInput.current?.click()}
        >
          <Sparkles />
          {busy === "summary" ? "Summarising…" : "Summarise from files"}
        </Button>
        <Button
          type="button"
          variant="outline"
          size="sm"
          disabled={disabled || busy !== null}
          onClick={() => setResearchOpen(true)}
        >
          <Globe />
          {busy === "research" ? "Researching…" : "Research"}
        </Button>
        <span className="text-xs text-muted-foreground">
          Attached files are read in full by every agent. A summary or research is written into the text above.
        </span>
      </div>
      <Dialog open={researchOpen} onOpenChange={(open) => busy !== "research" && setResearchOpen(open)}>
        <DialogContent className="sm:max-w-lg">
          <form
            className="flex flex-col gap-4"
            onSubmit={(e) => {
              e.preventDefault();
              research();
            }}
          >
            <DialogHeader>
              <DialogTitle>Research a topic</DialogTitle>
              <DialogDescription>
                A model searches the web and writes what it finds, with links to its sources, into the shared context.
                Every agent will read it.
              </DialogDescription>
            </DialogHeader>
            <div className="flex flex-col gap-2">
              <Label htmlFor="research-topic">Topic</Label>
              <Textarea
                id="research-topic"
                rows={3}
                autoFocus
                value={topic}
                disabled={busy === "research"}
                onChange={(e) => setTopic(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                    e.preventDefault();
                    research();
                  }
                }}
                placeholder="European PET resin prices in 2026 and the outlook for 2027"
              />
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" disabled={busy === "research"} onClick={() => setResearchOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={!topic.trim() || busy === "research"}>
                <Globe />
                {busy === "research" ? "Searching the web… (up to a minute)" : "Search the web"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
