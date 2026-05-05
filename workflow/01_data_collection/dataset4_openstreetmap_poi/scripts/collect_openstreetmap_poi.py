"""
Collect OpenStreetMap POI elements for the Emotion City Map dataset.

Dataset 4 uses OpenStreetMap / Overpass API as a live spatial data source.
It gathers named urban elements in London and maps OSM tags to emotional and
spatial parameters for later vectorisation, clustering, and 3D generation.

Example:
    python workflow\\01_data_collection\\dataset4_openstreetmap_poi\\scripts\\collect_openstreetmap_poi.py --target-items 300
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DATASET_DIR = Path(__file__).resolve().parents[1]
DEFAULT_QUERIES = DATASET_DIR / "osm_poi_queries.csv"
DEFAULT_OUT = DATASET_DIR / "outputs"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def read_queries(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def overpass_filter(osm_key: str, osm_value: str) -> str:
    if osm_value == "*":
        return f'["{osm_key}"]'
    return f'["{osm_key}"="{osm_value}"]'


def build_query(
    osm_key: str,
    osm_value: str,
    bbox: str,
    max_items: int,
    named_only: bool,
) -> str:
    tag_filter = overpass_filter(osm_key, osm_value)
    name_filter = '["name"]' if named_only else ""
    return f"""
    [out:json][timeout:60];
    (
      node{tag_filter}{name_filter}({bbox});
      way{tag_filter}{name_filter}({bbox});
      relation{tag_filter}{name_filter}({bbox});
    );
    out center tags {max_items};
    """


def request_overpass(query: str, retry_count: int = 3) -> dict[str, Any]:
    body = urlencode({"data": query}).encode("utf-8")
    for attempt in range(retry_count):
        req = Request(
            OVERPASS_URL,
            data=body,
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "User-Agent": "emotion-city-map-student-project/1.0",
            },
            method="POST",
        )
        try:
            with urlopen(req, timeout=90) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            error_text = exc.read().decode("utf-8", errors="replace")
            if exc.code in {429, 500, 502, 503, 504} and attempt < retry_count - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Overpass HTTP {exc.code}: {error_text}") from exc
        except URLError as exc:
            if attempt < retry_count - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Network error: {exc}") from exc

    raise RuntimeError("Overpass request failed after retries.")


def element_lat_lon(element: dict[str, Any]) -> tuple[Any, Any]:
    if "lat" in element and "lon" in element:
        return element["lat"], element["lon"]
    center = element.get("center") or {}
    return center.get("lat", ""), center.get("lon", "")


def normalise_element(element: dict[str, Any], query_row: dict[str, str]) -> dict[str, Any]:
    tags = element.get("tags") or {}
    lat, lon = element_lat_lon(element)
    element_uid = f"{element.get('type')}/{element.get('id')}"
    return {
        "element_id": element_uid,
        "dataset": "openstreetmap_poi",
        "source_website": "OpenStreetMap / Overpass API",
        "query_label": query_row["label"],
        "osm_type": element.get("type", ""),
        "osm_numeric_id": element.get("id", ""),
        "name": tags.get("name", ""),
        "osm_key": query_row["osm_key"],
        "osm_value": tags.get(query_row["osm_key"], query_row["osm_value"]),
        "category": query_row["category"],
        "emotion1": query_row["emotion1"],
        "emotion2": query_row["emotion2"],
        "value1": query_row["value1"],
        "value2": query_row["value2"],
        "latitude": lat,
        "longitude": lon,
        "amenity": tags.get("amenity", ""),
        "shop": tags.get("shop", ""),
        "leisure": tags.get("leisure", ""),
        "landuse": tags.get("landuse", ""),
        "office": tags.get("office", ""),
        "railway": tags.get("railway", ""),
        "tags_json": json.dumps(tags, ensure_ascii=False, sort_keys=True),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--target-items", type=int, default=300)
    parser.add_argument(
        "--bbox",
        default="51.28,-0.51,51.70,0.34",
        help="south,west,north,east. Default roughly covers Greater London.",
    )
    parser.add_argument("--sleep", type=float, default=1.0)
    parser.add_argument("--include-unnamed", action="store_true")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = args.out_dir / "raw"
    raw_dir.mkdir(exist_ok=True)

    rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for query_row in read_queries(args.queries):
        if len(rows) >= args.target_items:
            break

        max_items = int(query_row.get("max_items") or 50)
        print(f"Querying OSM: {query_row['label']}")
        query = build_query(
            query_row["osm_key"],
            query_row["osm_value"],
            args.bbox,
            max_items=max_items,
            named_only=not args.include_unnamed,
        )
        data = request_overpass(query)
        (raw_dir / f"{query_row['label']}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        time.sleep(args.sleep)

        for element in data.get("elements", []):
            element_uid = f"{element.get('type')}/{element.get('id')}"
            if element_uid in seen_ids:
                continue
            seen_ids.add(element_uid)
            rows.append(normalise_element(element, query_row))
            print(f"  items: {len(rows)} / {args.target_items}")
            if len(rows) >= args.target_items:
                break

    csv_path = args.out_dir / "openstreetmap_poi_dataset.csv"
    json_path = args.out_dir / "openstreetmap_poi_dataset.json"
    write_csv(csv_path, rows)
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Saved {len(rows)} OSM elements")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")


if __name__ == "__main__":
    main()
