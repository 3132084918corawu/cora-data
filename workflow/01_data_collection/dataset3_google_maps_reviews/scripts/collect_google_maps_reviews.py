"""
Collect Google Maps review text for the Emotion City Map dataset.

This uses the official Google Places API (New), rather than scraping the
Google Maps web interface. Place Details returns a small review sample per
place, so the script searches many places and combines their reviews.

Environment:
    GOOGLE_MAPS_API_KEY=your_key

Example:
    python scripts/collect_google_maps_reviews.py --target-reviews 300
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import time
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DATASET_DIR = Path(__file__).resolve().parents[1]
DEFAULT_QUERIES = DATASET_DIR / "google_maps_review_queries.csv"
DEFAULT_OUT = DATASET_DIR / "outputs"

SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
DETAILS_URL = "https://places.googleapis.com/v1/places/{place_id}"


def read_queries(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_api_key() -> str:
    key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if key:
        return key

    for env_path in (DATASET_DIR / ".env", DATASET_DIR.parents[2] / ".env"):
        if not env_path.is_file():
            continue
        for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            if name.strip() == "GOOGLE_MAPS_API_KEY":
                return value.strip().strip('"').strip("'")
    return ""


def request_json(
    url: str,
    api_key: str,
    field_mask: str,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    retry_count: int = 3,
) -> dict[str, Any]:
    body = None
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": field_mask,
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    for attempt in range(retry_count):
        req = Request(url, data=body, headers=headers, method=method)
        try:
            with urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            error_text = exc.read().decode("utf-8", errors="replace")
            if exc.code in {429, 500, 502, 503, 504} and attempt < retry_count - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Google API HTTP {exc.code}: {error_text}") from exc
        except URLError as exc:
            if attempt < retry_count - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Network error: {exc}") from exc

    raise RuntimeError("Request failed after retries.")


def search_places(api_key: str, query: str, page_size: int) -> list[dict[str, Any]]:
    payload = {
        "textQuery": query,
        "pageSize": page_size,
        "languageCode": "en",
    }
    field_mask = (
        "places.id,places.name,places.displayName,places.formattedAddress,"
        "places.types,places.rating,places.userRatingCount,places.location"
    )
    data = request_json(
        SEARCH_URL,
        api_key=api_key,
        field_mask=field_mask,
        method="POST",
        payload=payload,
    )
    return data.get("places", [])


def get_place_details(api_key: str, place_id: str) -> dict[str, Any]:
    field_mask = (
        "id,name,displayName,formattedAddress,types,rating,userRatingCount,"
        "location,reviews"
    )
    return request_json(
        DETAILS_URL.format(place_id=place_id),
        api_key=api_key,
        field_mask=field_mask,
    )


def text_value(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("text") or "")
    if value is None:
        return ""
    return str(value)


def normalise_review(
    review: dict[str, Any],
    place: dict[str, Any],
    query_row: dict[str, str],
) -> dict[str, Any] | None:
    original_text = text_value(review.get("originalText"))
    translated_text = text_value(review.get("text"))
    review_text = original_text or translated_text
    if not review_text.strip():
        return None

    place_name = text_value(place.get("displayName"))
    location = place.get("location") or {}
    author = review.get("authorAttribution") or {}
    place_id = place.get("id") or place.get("name", "").replace("places/", "")
    review_hash = hashlib.sha1(
        f"{place_id}|{author.get('displayName', '')}|{review_text}".encode("utf-8")
    ).hexdigest()[:16]

    return {
        "review_id": review_hash,
        "dataset": "google_maps_reviews",
        "source_website": "Google Maps / Google Places API",
        "query": query_row["query"],
        "place_id": place_id,
        "place_name": place_name,
        "place_address": place.get("formattedAddress", ""),
        "place_types": "|".join(place.get("types", [])),
        "place_rating": place.get("rating", ""),
        "place_user_rating_count": place.get("userRatingCount", ""),
        "latitude": location.get("latitude", ""),
        "longitude": location.get("longitude", ""),
        "review_rating": review.get("rating", ""),
        "review_publish_time": review.get("publishTime", ""),
        "review_relative_time": review.get("relativePublishTimeDescription", ""),
        "author_name": author.get("displayName", ""),
        "review_text": review_text.replace("\r", " ").replace("\n", " ").strip(),
        "category": query_row["category"],
        "emotion1": query_row["emotion1"],
        "emotion2": query_row["emotion2"],
        "value1": query_row["value1"],
        "value2": query_row["value2"],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "review_id",
        "dataset",
        "source_website",
        "query",
        "place_id",
        "place_name",
        "place_address",
        "place_types",
        "place_rating",
        "place_user_rating_count",
        "latitude",
        "longitude",
        "review_rating",
        "review_publish_time",
        "review_relative_time",
        "author_name",
        "review_text",
        "category",
        "emotion1",
        "emotion2",
        "value1",
        "value2",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(path: Path, rows: list[dict[str, Any]], target_reviews: int) -> None:
    category_counts = Counter(row["category"] for row in rows)
    query_counts = Counter(row["query"] for row in rows)
    summary = {
        "dataset": "google_maps_reviews",
        "target_reviews": target_reviews,
        "collected_reviews": len(rows),
        "category_counts": dict(category_counts),
        "query_counts": dict(query_counts),
        "unique_places": len({row["place_id"] for row in rows}),
        "note": (
            "Google Places Details returns a limited review sample per place, "
            "so this dataset combines reviews from many place searches."
        ),
    }
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--target-reviews", type=int, default=300)
    parser.add_argument("--places-per-query", type=int, default=20)
    parser.add_argument("--minimum-reviews", type=int, default=200)
    parser.add_argument("--sleep", type=float, default=0.15)
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        raise SystemExit(
            "Missing GOOGLE_MAPS_API_KEY. Set it in the terminal or add it to "
            "workflow/01_data_collection/dataset3_google_maps_reviews/.env"
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = args.out_dir / "raw"
    raw_dir.mkdir(exist_ok=True)

    rows: list[dict[str, Any]] = []
    seen_place_ids: set[str] = set()
    seen_review_ids: set[str] = set()

    for query_row in read_queries(args.queries):
        if len(rows) >= args.target_reviews:
            break

        print(f"Searching: {query_row['query']}")
        places = search_places(api_key, query_row["query"], args.places_per_query)
        time.sleep(args.sleep)

        for place in places:
            place_id = place.get("id")
            if not place_id or place_id in seen_place_ids:
                continue
            seen_place_ids.add(place_id)

            details = get_place_details(api_key, place_id)
            (raw_dir / f"{place_id}.json").write_text(
                json.dumps(details, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            time.sleep(args.sleep)

            for review in details.get("reviews", []):
                row = normalise_review(review, details, query_row)
                if row is None or row["review_id"] in seen_review_ids:
                    continue
                seen_review_ids.add(row["review_id"])
                rows.append(row)
                print(f"  reviews: {len(rows)} / {args.target_reviews}")
                if len(rows) >= args.target_reviews:
                    break

            if len(rows) >= args.target_reviews:
                break

    csv_path = args.out_dir / "google_maps_reviews_dataset.csv"
    json_path = args.out_dir / "google_maps_reviews_dataset.json"
    summary_path = args.out_dir / "google_maps_reviews_summary.json"
    write_csv(csv_path, rows)
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary(summary_path, rows, args.target_reviews)

    print(f"Saved {len(rows)} reviews")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")
    print(f"Summary: {summary_path}")
    if len(rows) < args.minimum_reviews:
        print(
            "WARNING: collected fewer than the required minimum. Add more queries "
            "or increase --places-per-query, then run again."
        )


if __name__ == "__main__":
    main()
