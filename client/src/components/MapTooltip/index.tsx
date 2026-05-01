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
      <div
        className="flex items-center gap-2 rounded-md px-2.5 py-1.5 shadow-xl"
        style={{
          backgroundColor: "#ffffff",
          border: "1px solid #e4dff5",
          boxShadow: "0 4px 12px rgba(109, 40, 217, 0.1)",
        }}
      >
        <span className="text-base leading-none" aria-hidden>
          {flag}
        </span>
        <span
          className="whitespace-nowrap text-xs font-medium"
          style={{ color: "#1e1b2e" }}
        >
          {name}
        </span>
      </div>
    </div>
  );
}

export { MapTooltip };
