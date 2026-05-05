# Dataset 3: Google Maps Reviews for an Emotional City Map

This dataset collects public review samples through the official Google Places
API. It is designed for the project theme: an emotional city map where parks are
interpreted as relaxed/open spaces and commercial areas are interpreted as
stressful/dense spaces.

## Files

- `google_maps_review_queries.csv` contains the search queries and emotional
  labels used to collect the reviews.
- `google_maps_reviews/google_maps_reviews_dataset.csv` is created after running
  the collection script.
- `google_maps_reviews/raw/` stores the raw Place Details JSON responses.

## How to Collect

Set a Google Maps Platform API key with Places API enabled. The target is 300
reviews, and the validation minimum is 200 reviews:

```powershell
$env:GOOGLE_MAPS_API_KEY="YOUR_KEY_HERE"
python workflow\01_data_collection\dataset3_google_maps_reviews\scripts\collect_google_maps_reviews.py --target-reviews 300 --minimum-reviews 200
```

The Google Places Details endpoint only returns a small sample of reviews for
each place, so the script searches many places and combines their reviews until
it reaches the target count.

If you prefer not to set the key globally, create this local file:

```text
workflow/01_data_collection/dataset3_google_maps_reviews/.env
```

with:

```text
GOOGLE_MAPS_API_KEY=YOUR_KEY_HERE
```

Do not upload `.env` to GitHub.

After collection, validate the dataset:

```powershell
python workflow\01_data_collection\dataset3_google_maps_reviews\scripts\validate_google_maps_reviews.py
```

## Role in the Workflow

Each review becomes one text element. The review is linked to:

- an urban category: `park relaxed` or `commercial stressful`
- an emotional axis: `calm -> stress`
- a spatial axis: `open -> dense`
- numerical design parameters: `value1` and `value2`

These fields can be vectorised with TF-IDF, Doc2Vec, or sentence embeddings.
The resulting clusters can then drive spatial rules such as height, spacing,
density, colour, distortion, and movement speed in Blender, Unreal, or
Processing.
