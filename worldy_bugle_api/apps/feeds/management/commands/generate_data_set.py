import json
import math
import warnings

import pycountry
import topojson
from django.core.management.base import BaseCommand
from shapely.geometry import Point

warnings.filterwarnings("ignore")


MANUAL_ISO = {
    "Turkey": "TUR",
    "S. Sudan": "SSD",
    "Somaliland": None,
    "Solomon Is.": "SLB",
    "St. Vin. and Gren.": "VCT",
    "St. Kitts and Nevis": "KNA",
    "Cook Is.": "COK",
    "W. Sahara": "ESH",
    "Fr. Polynesia": "PYF",
    "Eq. Guinea": "GNQ",
    "Dominican Rep.": "DOM",
    "Faeroe Is.": "FRO",
    "N. Cyprus": None,
    "Dem. Rep. Congo": "COD",
    "Central African Rep.": "CAF",
    "Bosnia and Herz.": "BIH",
    "Antigua and Barb.": "ATG",
    "Marshall Is.": "MHL",
    "N. Mariana Is.": "MNP",
    "U.S. Virgin Is.": "VIR",
    "Falkland Is.": "FLK",
    "Cayman Is.": "CYM",
    "British Virgin Is.": "VGB",
    "Turks and Caicos Is.": "TCA",
    "Wallis and Futuna Is.": "WLF",
    "St. Pierre and Miquelon": "SPM",
    "S. Geo. and the Is.": "SGS",
    "Br. Indian Ocean Ter.": "IOT",
    "Pitcairn Is.": "PCN",
    "Fr. S. Antarctic Lands": "ATF",
    "Siachen Glacier": None,
    "Ashmore and Cartier Is.": None,
    "Indian Ocean Ter.": None,
    "Heard I. and McDonald Is.": "HMD",
    "St-Martin": "MAF",
    "St-Barthélemy": "BLM",
}


class Command(BaseCommand):
    help = "Generate world hex dataset with country coordinates"

    HEX_R = 1.2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.HEX_W = self.HEX_R * math.sqrt(3)
        self.V_STEP = self.HEX_R * 1.5

    def add_arguments(self, parser):
        parser.add_argument(
            "--dataset",
            type=str,
            default="fixtures/countries_dataset/countries-50m.json",  # 50m, pas 110m
            help="Path to the input TopoJSON (countries-50m.json recommandé)",
        )
        parser.add_argument(
            "--output",
            type=str,
            default="fixtures/countries_dataset_output/world_hex_dataset.json",
            help="Path to save the generated dataset",
        )
        parser.add_argument(
            "--simplify",
            type=float,
            default=0.15,
            help="Geometry simplification tolerance in degrees (default: 0.15)",
        )
        return super().add_arguments(parser)

    def get_iso3(self, name):
        if name in MANUAL_ISO:
            return MANUAL_ISO[name]
        try:
            return pycountry.countries.search_fuzzy(name)[0].alpha_3
        except LookupError:
            return None

    def colrow_to_lonlat(self, col, row):
        offset = (self.HEX_W / 2) if (row % 2 == 1) else 0
        lon = col * self.HEX_W + offset - 180
        lat = 90 - row * self.V_STEP
        return lon, lat

    def lonlat_to_colrow(self, lon, lat):
        row_i = round((90 - lat) / self.V_STEP)
        offset = (self.HEX_W / 2) if (row_i % 2 == 1) else 0
        col_i = round((lon + 180 - offset) / self.HEX_W)
        return col_i, row_i

    def handle(self, *args, **options):
        self.stdout.write("Loading TopoJSON...")
        with open(options["dataset"]) as f:
            topo_raw = json.load(f)

        gdf = topojson.Topology(topo_raw, object_name="countries").to_gdf()
        gdf = gdf.set_crs("EPSG:4326")

        gdf["iso_a3"] = gdf["name"].apply(self.get_iso3)
        gdf = gdf[gdf["iso_a3"].notna()].copy()
        self.stdout.write(f"Countries with iso_a3: {len(gdf)}")

        result = []
        for _, country in gdf.iterrows():
            geom = country.geometry.simplify(options["simplify"])
            if geom.is_empty:
                continue

            b = geom.bounds
            col_min, row_max = self.lonlat_to_colrow(
                b[0] - self.HEX_W, b[1] - self.V_STEP
            )
            col_max, row_min = self.lonlat_to_colrow(
                b[2] + self.HEX_W, b[3] + self.V_STEP
            )

            hexes = []
            for row in range(max(0, row_min - 1), min(110, row_max + 2)):
                for col in range(max(0, col_min - 1), min(185, col_max + 2)):
                    lon, lat = self.colrow_to_lonlat(col, row)
                    if geom.contains(Point(lon, lat)):
                        hexes.append([col, row])

            if len(hexes) == 0:
                centroid = country.geometry.centroid
                c, r = self.lonlat_to_colrow(centroid.x, centroid.y)
                hexes = [[c, r]]

            result.append(
                {
                    "name": country["name"],
                    "iso_a3": country["iso_a3"],
                    "hexes": hexes,
                }
            )

        with open(options["output"], "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        total_hexes = sum(len(c["hexes"]) for c in result)
        self.stdout.write(
            self.style.SUCCESS(
                f"Done: {len(result)} countries, {total_hexes} hexes total → {options['output']}"
            )
        )
