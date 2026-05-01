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
          backgroundColor: "#1f2028",
          border: "1px solid #2e303a",
          backdropFilter: "blur(4px)",
        }}
      >
        <span className="text-base leading-none" aria-hidden>
          {flag}
        </span>
        <span
          className="whitespace-nowrap text-xs font-medium"
          style={{ color: "#f3f4f6" }}
        >
          {name}
        </span>
      </div>
    </div>
  );
}

export { MapTooltip };
