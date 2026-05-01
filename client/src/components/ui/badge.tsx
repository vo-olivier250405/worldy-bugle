import type { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "outline";
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        variant === "default" && "bg-[#ede9fe] text-[#7c3aed]",
        variant === "outline" && "border border-[#e4dff5] text-[#9791a8]",
        className,
      )}
      {...props}
    />
  );
}

export { Badge };
