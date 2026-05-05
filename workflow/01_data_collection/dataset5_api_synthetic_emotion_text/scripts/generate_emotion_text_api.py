"""
Generate structured synthetic emotion observations using the OpenAI API.

This script is for Part 1.3 of the coursework. It augments the scraped / API
datasets with structured design text: sensory observation, emotion reading,
and spatial rules.

Example:
    python workflow\\01_data_collection\\dataset5_api_synthetic_emotion_text\\scripts\\generate_emotion_text_api.py --items-per-category 40
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

from openai import OpenAI


DATASET_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = DATASET_DIR / "outputs"

CATEGORIES = [
    {
        "category": "park relaxed",
        "emotion1": "calm",
        "emotion2": "open",
        "value1": 0.20,
        "value2": 0.10,
        "brief": "public park, garden, riverside walk, soft air, slow walking, open edges",
    },
    {
        "category": "commercial stressful",
        "emotion1": "stress",
        "emotion2": "dense",
        "value1": 0.90,
        "value2": 0.80,
        "brief": "shopping street, office district, market, crowding, visual overload, fast movement",
    },
    {
        "category": "transport tense",
        "emotion1": "tense",
        "emotion2": "fast",
        "value1": 0.75,
        "value2": 0.65,
        "brief": "station, interchange, platform, compressed waiting, directional flow, timetable pressure",
    },
]


def make_prompt(category: dict[str, object], count: int) -> str:
    return f"""
Create {count} unique structured observations for an architectural design dataset.
Theme: an emotional city map.
Urban category: {category['category']}
Emotional/spatial condition: {category['emotion1']} / {category['emotion2']}
Context hints: {category['brief']}

Return only JSON as a list. Each item must have:
- sensory_observer: 1 sentence, concrete and spatial
- emotional_interpreter: 1 sentence explaining the emotion
- spatial_rule: 1 sentence translating emotion into geometry
- keywords: 5 short comma-separated keywords
Avoid repeating phrases across items.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items-per-category", type=int, default=40)
    parser.add_argument("--model", default="gpt-4.1-mini")
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Missing OPENAI_API_KEY. Set it before running this script.")

    client = OpenAI()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []

    for category in CATEGORIES:
        response = client.responses.create(
            model=args.model,
            input=make_prompt(category, args.items_per_category),
        )
        content = response.output_text
        items = json.loads(content)
        for index, item in enumerate(items, start=1):
            rows.append(
                {
                    "item_id": f"{category['category'].replace(' ', '_')}_{index:03d}",
                    "dataset": "api_synthetic_emotion_text",
                    "source_api": "OpenAI Responses API",
                    "category": category["category"],
                    "emotion1": category["emotion1"],
                    "emotion2": category["emotion2"],
                    "value1": category["value1"],
                    "value2": category["value2"],
                    "sensory_observer": item["sensory_observer"],
                    "emotional_interpreter": item["emotional_interpreter"],
                    "spatial_rule": item["spatial_rule"],
                    "keywords": item["keywords"],
                }
            )

    csv_path = OUT_DIR / "api_emotion_text_dataset.csv"
    json_path = OUT_DIR / "api_emotion_text_dataset.json"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(rows)} API-generated items")
    print(csv_path)


if __name__ == "__main__":
    main()
