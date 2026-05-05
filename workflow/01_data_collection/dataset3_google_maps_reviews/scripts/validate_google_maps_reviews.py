"""
Validate Dataset 3 against the 200-300 element requirement.

Example:
    python workflow\\01_data_collection\\dataset3_google_maps_reviews\\scripts\\validate_google_maps_reviews.py
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


DATASET_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CSV = DATASET_DIR / "outputs" / "google_maps_reviews_dataset.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--minimum", type=int, default=200)
    parser.add_argument("--maximum", type=int, default=300)
    args = parser.parse_args()

    if not args.csv.exists():
        raise SystemExit(f"Dataset CSV not found: {args.csv}")

    with args.csv.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)
    categories = Counter(row.get("category", "") for row in rows)
    unique_places = len({row.get("place_id", "") for row in rows})
    empty_reviews = sum(1 for row in rows if not row.get("review_text", "").strip())

    print(f"Dataset: {args.csv}")
    print(f"Total reviews: {total}")
    print(f"Required range: {args.minimum}-{args.maximum}")
    print(f"Unique places: {unique_places}")
    print(f"Empty review texts: {empty_reviews}")
    print("Category counts:")
    for category, count in categories.most_common():
        print(f"  {category}: {count}")

    if args.minimum <= total <= args.maximum and empty_reviews == 0:
        print("Status: PASS")
    else:
        print("Status: NEEDS MORE DATA")


if __name__ == "__main__":
    main()
