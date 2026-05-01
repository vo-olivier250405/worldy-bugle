import type { FC } from "react";
import worldData from "../assets/world.json";

export interface WorldMapProps {
  articleCounts: Record<string, number>;
}

const HEX_PX = 6.5;
const HEX_W = HEX_PX * Math.sqrt(3);
const V_STEP = HEX_PX * 1.5;
const COL_MIN = 1;
const ROW_MIN = 4;
const PAD = 10;

function hexCenter(col: number, row: number) {
  const offset = row % 2 === 1 ? HEX_W / 2 : 0;
  return {
    x: (col - COL_MIN) * HEX_W + offset + PAD,
    y: (row - ROW_MIN) * V_STEP + PAD,
  };
}

function hexPoints(cx: number, cy: number, r: number) {
  return Array.from({ length: 6 }, (_, i) => {
    const angle = (Math.PI / 180) * (60 * i - 30);
    return `${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`;
  }).join(" ");
}

const WorldMap: FC = () => {
  return (
    <svg viewBox="...">
      {worldData.map((country) =>
        country.hexes.map(([col, row]) => {
          const { x, y } = hexCenter(col, row);
          return (
            <polygon
              key={`${country.iso_a3}-${col}-${row}`}
              points={hexPoints(x, y, HEX_PX - 0.8)}
              data-iso={country.iso_a3}
              className="hex"
            />
          );
        }),
      )}
    </svg>
  );
};

export default WorldMap;
