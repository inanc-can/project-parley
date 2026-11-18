"use client"

import * as React from "react"
import { cn } from "cn"

function Label({ className, ...props }: React.ComponentProps<"label">) {
  return (
    <label
      data-slot="label"
      className={cn(
        "flex items-center gap-2 font-mono text-[0.7rem] leading-none font-medium tracking-[0.08em] text-muted-foreground uppercase select-none has-data-[slot=checkbox]:font-sans has-data-[slot=checkbox]:text-sm has-data-[slot=checkbox]:tracking-normal has-data-[slot=checkbox]:text-foreground has-data-[slot=checkbox]:normal-case has-data-[slot=switch]:font-sans has-data-[slot=switch]:text-sm has-data-[slot=switch]:tracking-normal has-data-[slot=switch]:text-foreground has-data-[slot=switch]:normal-case group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
        className
      )}
      {...props}
    />
  )
}

export { Label }
