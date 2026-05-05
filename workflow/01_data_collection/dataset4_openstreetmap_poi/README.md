# Dataset 4: OpenStreetMap POI Data

This dataset uses OpenStreetMap urban point-of-interest data through the
Overpass API. It is different from the Pinterest image datasets and the Google
Maps review dataset because it provides live spatial/categorical city data
rather than images or reviews.

## Files

- `osm_poi_queries.csv` defines the OSM tags and emotional/spatial labels.
- `scripts/collect_openstreetmap_poi.py` collects the dataset.
- `outputs/openstreetmap_poi_dataset.csv` is created after running the script.
- `outputs/raw/` stores the raw Overpass JSON responses.

## How to Collect

No API key is needed:

```powershell
python workflow\01_data_collection\dataset4_openstreetmap_poi\scripts\collect_openstreetmap_poi.py --target-items 500
```

The default bounding box covers Greater London. To use another city, pass a
bounding box in `south,west,north,east` order:

```powershell
python workflow\01_data_collection\dataset4_openstreetmap_poi\scripts\collect_openstreetmap_poi.py --bbox "51.28,-0.51,51.70,0.34" --target-items 500
```

## Current Collected Output

The current output contains 500 OSM elements:

- `park relaxed`: 280 elements
- `commercial stressful`: 220 elements

The collected query groups are parks, gardens, green spaces, shops, and offices.

## Role in the Workflow

Each OSM element becomes one spatial data item. It includes:

- name and OSM tags
- latitude and longitude
- urban category: `park relaxed`, `commercial stressful`, or `transport tense`
- emotional axis: `calm`, `stress`, or `tense`
- spatial axis: `open`, `dense`, or `fast`
- numerical parameters: `value1` and `value2`

For the emotional city map, this dataset can be used to place generated
fragments geographically. Parks can become low, open, slow spatial fragments;
commercial POIs can become dense, tall, fragmented structures; transport POIs
can become fast transitional corridors.

## Attribution

Data source: OpenStreetMap contributors, accessed through the Overpass API.
OpenStreetMap data is available under the Open Database License.
