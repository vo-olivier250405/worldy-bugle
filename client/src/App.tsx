import { useState, useCallback } from "react";
import WorldMap from "./components/WorldMap";
import { CountrySheet } from "./components/CountrySheet";
import { MapTooltip } from "./components/MapTooltip";

interface SelectedCountry {
  iso: string;
  name: string;
}

interface TooltipState {
  iso: string;
  name: string;
  x: number;
  y: number;
}

function App() {
  const [selected, setSelected] = useState<SelectedCountry | null>(null);
  const [tooltip, setTooltip] = useState<TooltipState | null>(null);

  const handleCountryClick = useCallback((iso: string, name: string) => {
    setSelected({ iso, name });
  }, []);

  const handleClose = useCallback(() => setSelected(null), []);

  const handleCountryHover = useCallback(
    (iso: string | null, name: string | null, x: number, y: number) => {
      if (iso && name) {
        setTooltip({ iso, name, x, y });
      } else {
        setTooltip(null);
      }
    },
    [],
  );

  return (
    <div className="flex h-svh flex-col bg-background">
      <header className="flex h-13 shrink-0 items-center px-6 border-b border-border bg-surface">
        <span className="text-sm font-semibold uppercase tracking-widest text-heading">
          Worldy Bugle
        </span>
      </header>

      <main className="flex flex-1 items-center justify-center overflow-hidden p-6">
        <WorldMap
          selectedIso={selected?.iso ?? null}
          onCountryClick={handleCountryClick}
          onCountryHover={handleCountryHover}
        />
      </main>

      {tooltip && (
        <MapTooltip
          iso={tooltip.iso}
          name={tooltip.name}
          x={tooltip.x}
          y={tooltip.y}
        />
      )}

      <CountrySheet
        iso={selected?.iso ?? null}
        countryName={selected?.name ?? null}
        onClose={handleClose}
      >
        <CountrySheet.Header />
        <CountrySheet.ArticleList />
      </CountrySheet>
    </div>
  );
}

export default App;
