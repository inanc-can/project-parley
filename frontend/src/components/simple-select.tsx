"use client";

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

type Option = { value: string; label?: string };

// A value/onChange select over the Base UI primitives.
export function SimpleSelect({
  value,
  onChange,
  options,
  disabled,
  className,
}: {
  value: string;
  onChange: (v: string) => void;
  options: Option[];
  disabled?: boolean;
  className?: string;
}) {
  const items = Object.fromEntries(options.map((o) => [o.value, o.label ?? o.value]));
  return (
    <Select value={value} items={items} disabled={disabled} onValueChange={(v) => v != null && onChange(String(v))}>
      <SelectTrigger className={className ?? "w-full"}>
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        {options.map((o) => (
          <SelectItem key={o.value} value={o.value}>
            {o.label ?? o.value}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
