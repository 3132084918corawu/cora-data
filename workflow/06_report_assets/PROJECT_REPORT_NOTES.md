# Emotion City Map: Project Report Notes

## Goal

The project transforms machine-learning outputs into design-driving systems for
spatial generation. The theme is an emotional city map: parks are interpreted as
relaxed/open spaces, commercial areas as stressful/dense spaces, and transport
nodes as tense/fast transitional spaces.

## Part 1.1 Data Collection

Dataset 1: Pinterest park images

- Source: Pinterest
- Folder: `photos1/`
- Count: 200 image files, 188 readable images
- Role: visual reference for relaxed/open urban atmospheres

Dataset 2: Pinterest business environment images

- Source: Pinterest
- Folder: `photos2/`
- Count: 200 image files, 199 readable images
- Role: visual reference for commercial/stressful urban atmospheres

Dataset 3: Google Maps reviews

- Source: Google Maps / Google Places API
- Folder: `workflow/01_data_collection/dataset3_google_maps_reviews/`
- Status: collector and validator prepared
- Requirement note: this requires `GOOGLE_MAPS_API_KEY`; run the collector to
  generate 200-300 real review records.

Dataset 4: OpenStreetMap POI data

- Source: OpenStreetMap / Overpass API
- Output: `workflow/01_data_collection/dataset4_openstreetmap_poi/outputs/openstreetmap_poi_dataset.csv`
- Count: 500 elements
- Categories: 280 `park relaxed`, 220 `commercial stressful`
- Role: real city locations and tags that connect emotion to geographic space

Dataset 5: API-generated emotion text

- Source: OpenAI API
- Folder: `workflow/01_data_collection/dataset5_api_synthetic_emotion_text/`
- Status: script prepared; requires `OPENAI_API_KEY`
- Role: augments the scraped/API datasets with structured sensory observation,
  emotional interpretation, and spatial rules.

## Part 1.2 Vectorisation

Text vectorisation uses the OpenStreetMap POI names and tags.

- Method A: TF-IDF + SVD
- Method B: HashingVectorizer + SVD
- Output: `workflow/02_vectorisation/outputs/text_vectorisation_tfidf_vs_hashing.csv`

Why TF-IDF:

TF-IDF is readable and explainable. It makes it possible to identify which words
and tags contribute to the emotional categories. This is useful for a design
report because terms such as park, garden, office, and shop can be linked back
to design rules.

Why HashingVectorizer:

HashingVectorizer is fast and scalable. It does not store a vocabulary, so it is
less interpretable than TF-IDF, but it can process larger text streams with a
stable feature size.

Result from this dataset:

- TF-IDF silhouette: 0.235
- Hashing silhouette: 0.109
- TF-IDF gave clearer clusters for this small/medium tagged urban dataset.

Image vectorisation uses Pinterest image pixels.

- Method A: colour statistics and colour histograms
- Method B: colour + texture/edge features
- Output: `workflow/02_vectorisation/outputs/image_vectorisation_colour_texture.csv`

Result from this dataset:

- Valid images: 387
- Colour feature silhouette: 0.306
- Colour + texture silhouette: 0.251
- Colour and texture clusters were similar, with ARI 0.822. This suggests the
  park/commercial image difference is strongly carried by colour and brightness,
  while texture adds detail but also noise.

## Part 1.3 API Interaction

The API interaction script is:

`workflow/01_data_collection/dataset5_api_synthetic_emotion_text/scripts/generate_emotion_text_api.py`

It generates structured JSON/CSV records with:

- sensory observer
- emotional interpreter
- spatial rule
- keywords

This step requires the user's `OPENAI_API_KEY`. It has not been executed here
because no API key is available in the environment.

## Part 1.4 Machine Learning

Two machine-learning models were compared on OSM vector and emotion-space
features.

Model 1: KMeans clustering

- Output: `workflow/03_machine_learning/outputs/osm_ml_clusters_kmeans_vs_gmm.csv`
- Silhouette: 0.635

Model 2: Gaussian Mixture Model

- Output: same CSV
- Silhouette: 0.494

Comparison:

KMeans performed better for this dataset because the design labels use clear
numerical parameter bands: relaxed/open has low `value1/value2`, while
commercial/stressful has high `value1/value2`. GMM produced softer clusters,
which is conceptually useful for mixed emotional zones but less separated in the
current feature space.

A RandomForest classifier was also used as a checking step. It predicted the two
main emotional categories with 1.0 accuracy because the dataset currently has
very explicit emotional labels and parameter values.

## Part 1.5 Visualisation

Matplotlib and Seaborn figures are stored in:

`workflow/04_visualisation/outputs/`

Key figures:

- `01_osm_category_query_counts.png`
- `02_text_tfidf_svd_clusters.png`
- `03_text_hashing_svd_clusters.png`
- `04_image_colour_texture_pca.png`
- `05_kmeans_emotion_space.png`
- `06_gmm_text_space.png`
- `07_category_cluster_heatmap.png`
- `08_fragment_parameter_variation.png`

## Part 2.1 Project Brief

The design workflow uses multiple environments:

1. Python: data cleaning, vectorisation, clustering, and fragment parameter
   generation.
2. Cinema 4D: 3D architectural fragment generation and 60-second animation.
3. Processing: interactive P3D animation using the same fragment CSV.
4. Unreal or Blender: optional environments for spawning the same fragments as
   actors.

## Part 2.2 Integrated Workflows

Workflow A: Image and OSM data to Cinema 4D

Pinterest images are vectorised into colour/texture features. OSM tags are
vectorised into text embeddings. Machine-learning clusters generate spatial
parameters, and Cinema 4D reads the final fragment CSV to create animated 3D
blocks.

Workflow B: OSM emotion parameters to Processing

OSM category and cluster outputs become height, density, colour, distortion,
and speed. Processing reads the same CSV and creates a moving emotional city
field.

Workflow C: OSM locations to Unreal

The Unreal script reads the same CSV and spawns cube actors with category-driven
scale and material colour. This allows the same dataset to move into a
real-time engine.

## Part 2.3 Iterative Reconfiguration

Fragment parameter file:

`workflow/05_design_tool_integration/fragment_parameters/emotion_city_fragments_32.csv`

The final system contains 32 architectural fragments. Each fragment has:

- source POI
- emotional category
- KMeans and GMM cluster IDs
- height, width, depth, spacing
- distortion and movement speed
- RGB colour
- scene position

The fragments are not isolated objects. They are systematic variations generated
from the same emotional and machine-learning rules.

## Part 2.4 3D Scenes and Animation

Cinema 4D script:

`workflow/05_design_tool_integration/cinema4d/generate_emotion_city_c4d.py`

This script creates 32 3D fragments and sets a 1800-frame animation at 30 fps,
which equals 60 seconds.

Processing script:

`workflow/05_design_tool_integration/processing/emotion_city_fragments_animation.pde`

This script creates an animated P3D view of the same fragments.

Unreal script:

`workflow/05_design_tool_integration/unreal/generate_emotion_city_fragments_unreal.py`

This script can spawn the same fragments in Unreal Editor.

Preview animation:

`workflow/06_report_assets/emotion_city_preview_65s.mp4`

This preview is 65 seconds long and was generated from the fragment CSV. It can
be used as a quick report/crit preview while the higher-quality Blender render
is prepared.
