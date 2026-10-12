import { toast } from "@/components/ui/toast";

// One place for user-facing notifications, so they look and read the same everywhere.

export function notifyError(e: unknown, title = "That didn't work") {
  toast.add({ title, description: e instanceof Error ? e.message : String(e), type: "error" });
}

export function notifySuccess(title: string, description?: string) {
  toast.add({ title, description, type: "success" });
}

export function notifyInfo(title: string, description?: string) {
  toast.add({ title, description, type: "info" });
}

// Run an action; toast its error, or its success message if one is given.
export async function attempt(fn: () => Promise<unknown>, success?: string, errorTitle?: string) {
  try {
    await fn();
    if (success) notifySuccess(success);
    return true;
  } catch (e) {
    notifyError(e, errorTitle);
    return false;
  }
}
