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
    (
      iso: string | null,
      name: string | null,
      x: number,
      y: number,
    ) => {
      if (iso && name) {
        setTooltip({ iso, name, x, y });
      } else {
        setTooltip(null);
      }
    },
    [],
  );

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100svh",
        backgroundColor: "#16171d",
      }}
    >
      {/* Header */}
      <header
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          padding: "0 24px",
          height: "52px",
          flexShrink: 0,
          borderBottom: "1px solid #2e303a",
        }}
      >
        <span
          style={{
            fontSize: "14px",
            fontWeight: 600,
            letterSpacing: "0.1em",
            color: "#f3f4f6",
            textTransform: "uppercase",
          }}
        >
          Worldy Bugle
        </span>
        <span
          style={{
            fontSize: "10px",
            fontWeight: 500,
            letterSpacing: "0.18em",
            color: "#c084fc",
            textTransform: "uppercase",
            opacity: 0.75,
          }}
        >
          Geopolitical Intelligence
        </span>
      </header>

      {/* Map */}
      <main
        style={{
          flex: 1,
          overflow: "hidden",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "24px",
        }}
      >
        <WorldMap
          selectedIso={selected?.iso ?? null}
          onCountryClick={handleCountryClick}
          onCountryHover={handleCountryHover}
        />
      </main>

      {/* Tooltip */}
      {tooltip && (
        <MapTooltip
          iso={tooltip.iso}
          name={tooltip.name}
          x={tooltip.x}
          y={tooltip.y}
        />
      )}

      {/* Side sheet */}
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
