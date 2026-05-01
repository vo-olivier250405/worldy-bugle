import { getCountryFlag } from "@/lib/isoMap";

interface MapTooltipProps {
  iso: string;
  name: string;
  x: number;
  y: number;
}

function MapTooltip({ iso, name, x, y }: MapTooltipProps) {
  const flag = getCountryFlag(iso);

  return (
    <div
      className="pointer-events-none fixed z-50"
      style={{ left: x + 14, top: y - 44 }}
    >
      <div className="flex items-center gap-2 rounded-md border border-border bg-surface px-2.5 py-1.5 shadow-[0_4px_12px_rgba(109,40,217,0.1)]">
        <span className="text-base leading-none" aria-hidden>
          {flag}
        </span>
        <span className="whitespace-nowrap text-xs font-medium text-heading">
          {name}
        </span>
      </div>
    </div>
  );
}

export { MapTooltip };
