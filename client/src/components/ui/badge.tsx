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
        variant === "default" && "bg-[#2a1f45] text-[#c084fc]",
        variant === "outline" && "border border-[#2e303a] text-[#9ca3af]",
        className,
      )}
      {...props}
    />
  );
}

export { Badge };
