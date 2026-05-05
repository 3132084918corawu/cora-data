# Emotion City Map

## Transforming Urban Emotions into Data-Driven Spatial Systems

Student: Kaiying Huang  
Project theme: An emotional map of the city  
Core idea: park = relaxed/open, commercial = stressful/dense, transport = tense/fast  
Software environments: Python, Cinema 4D, Processing

![OSM category counts](E:/11.python%20work/cora-data/workflow/06_report_assets/01_osm_category_query_counts.png)

---

# Project Status

## Goal

This project transforms machine-learning outputs, including vector embeddings,
clusters, and emotional parameters, into design-driving systems for spatial
generation. The project asks how a city can be read as an emotional field. Parks
are interpreted as relaxed and open, commercial areas as stressful and dense,
and transport nodes as tense and fast.

The final design outcome is an emotional city generator. Each emotional
condition becomes a spatial rule:

- Relaxed / open: lower height, wider spacing, slower movement, blue-green tone.
- Stressful / dense: taller height, tighter spacing, faster movement, red-orange tone.
- Tense / fast: directional movement, transitional rhythm, compressed corridors.

The workflow links data collection, vectorisation, machine learning,
visualisation, and 3D generation. The data does not remain as analysis only. It
is translated into 32 architectural fragments and animated as a one-minute
spatial system.

---

# Part 1: Projecting Between Domains

## 1.1 Web Scraping and Data Collection

The project uses three main datasets from two different domains: Pinterest image
data and OpenStreetMap urban point data. A Google Maps review collector is also
prepared as an optional extension that can be run with an API key.

## Dataset 1: Park / Relaxed Image Dataset

Source: Pinterest  
Domain: image / social media image search  
Folder: `photos1/`  
Metadata: `metadata/pinterest_future_city_metadata.csv`  
Collected elements: 200 image files  
Readable images used in analysis: 188

This dataset represents relaxed and open urban atmospheres. It contains park,
garden, landscape, and green-space references. In the design logic, these images
support the low-density, slow-moving, open spatial condition.

## Dataset 2: Commercial / Stressful Image Dataset

Source: Pinterest  
Domain: image / social media image search  
Folder: `photos2/`  
Metadata: `metadata/pinterest_business environment_metadata.csv`  
Collected elements: 200 image files  
Readable images used in analysis: 199

This dataset represents dense commercial atmospheres. It includes business
environments, shopping areas, office-like environments, and visually busier
urban references. In the design logic, these images support the high-density,
compressed, vertical, and fast-moving condition.

## Dataset 3: OpenStreetMap Urban POI Dataset

Source: OpenStreetMap / Overpass API  
Domain: live spatial / urban point data  
Output: `workflow/01_data_collection/dataset4_openstreetmap_poi/outputs/openstreetmap_poi_dataset.csv`  
Collected elements: 500

Category distribution:

- `park relaxed`: 280
- `commercial stressful`: 220

The OpenStreetMap dataset contains real urban elements with names, tags,
coordinates, and category labels. It gives the project a spatial anchor: instead
of only using atmosphere images, the system also works with actual city
locations such as parks, gardens, shops, and offices.

Google Maps Review Extension:

The Google Maps review collector is located at:

`workflow/01_data_collection/dataset3_google_maps_reviews/`

It is prepared to collect 200-300 real review records using the Google Places
API, but it requires `GOOGLE_MAPS_API_KEY`. Since no key was available in this
environment, the review dataset is documented as a prepared extension rather
than used as a generated result.

---

## 1.2 Dataset Vectorisation

Vectorisation was used to translate both image and text/spatial datasets into
machine-readable feature spaces.

## Text / POI Vectorisation

Input dataset: OpenStreetMap POI names and tags  
Output: `workflow/02_vectorisation/outputs/text_vectorisation_tfidf_vs_hashing.csv`

Two vectorisation methods were compared:

1. TF-IDF + SVD
2. HashingVectorizer + SVD

TF-IDF was selected because it is interpretable. It allows the report to connect
words and OSM tags such as `park`, `garden`, `shop`, and `office` back to design
decisions. This is useful for a design workflow because the features are not a
black box.

HashingVectorizer was selected as a comparison because it is faster and more
scalable. It does not store a vocabulary, so it is less readable, but it can
process larger streams of text with a fixed feature size.

Result:

- TF-IDF silhouette: 0.235
- Hashing silhouette: 0.109
- Cluster agreement between both methods: ARI 0.490

Interpretation:

TF-IDF performed better for this dataset. OSM tags are short and structured, so
the vocabulary itself is meaningful. Hashing was faster but less interpretable
and produced weaker separation.

![TF-IDF clusters](E:/11.python%20work/cora-data/workflow/06_report_assets/02_text_tfidf_svd_clusters.png)

![Hashing clusters](E:/11.python%20work/cora-data/workflow/06_report_assets/03_text_hashing_svd_clusters.png)

## Image Vectorisation

Input datasets: Pinterest park images and Pinterest business images  
Output: `workflow/02_vectorisation/outputs/image_vectorisation_colour_texture.csv`

Two image vectorisation strategies were compared:

1. Colour statistics and HSV histograms
2. Colour + texture / edge features

Colour features were selected because the emotional contrast between park and
commercial atmospheres is partly visual: parks tend to contain green-blue,
softer, and more open images; commercial environments tend to contain stronger
contrast, hard surfaces, signage, glass, and artificial lighting.

Texture and edge features were added as a comparison because commercial spaces
often have more hard boundaries, visual clutter, and sharper geometry.

Result:

- Valid images: 387
- Colour feature silhouette: 0.306
- Colour + texture feature silhouette: 0.251
- Cluster agreement: ARI 0.822

Interpretation:

Colour separated the datasets more strongly than texture. Texture added detail,
but also noise, because some park images include paths, buildings, and hard
edges, while some commercial images have smooth surfaces.

![Image PCA](E:/11.python%20work/cora-data/workflow/06_report_assets/04_image_colour_texture_pca.png)

---

## 1.3 API Interaction for Structured Data Retrieval

The API interaction component is prepared in:

`workflow/01_data_collection/dataset5_api_synthetic_emotion_text/scripts/generate_emotion_text_api.py`

This script uses the OpenAI API to generate structured emotional city
observations. Each generated item includes:

- sensory observation
- emotional interpretation
- spatial rule
- keywords

The script is designed to augment the scraped and spatial datasets. It creates
text that directly connects emotion to spatial grammar, for example:

- relaxed park atmosphere -> horizontal expansion, wide spacing, slow rhythm
- stressful commercial atmosphere -> vertical pressure, dense grid, fast rhythm
- tense transport atmosphere -> directional corridors and compressed waiting

This part requires the user's own `OPENAI_API_KEY`. The script is included and
ready, but no API key is stored in the project.

---

## 1.4 Machine Learning

Two machine-learning models were trained and compared using the OSM POI dataset
and vectorised features.

Input:

`workflow/03_machine_learning/outputs/osm_ml_clusters_kmeans_vs_gmm.csv`

Feature columns:

- value1
- value2
- TF-IDF SVD x/y
- Hashing SVD x/y

## Model 1: KMeans Clustering

KMeans was used to group urban elements into emotion-space clusters. It is
suitable for this project because the design system needs clear cluster labels
that can be mapped into spatial rules.

Result:

- KMeans silhouette: 0.635

## Model 2: Gaussian Mixture Model

Gaussian Mixture Model was used as a softer clustering comparison. Unlike
KMeans, GMM assumes data can belong to probabilistic distributions. This is
conceptually useful for emotional ambiguity, where a place might be partly calm
and partly stressful.

Result:

- GMM silhouette: 0.494

Comparison:

KMeans performed better in this dataset because the emotional parameters were
clearly separated: relaxed/open elements have low `value1/value2`, while
commercial/stressful elements have high `value1/value2`. GMM is still valuable
as a design idea because it supports transitional emotional zones, but KMeans
produced cleaner clusters for direct fragment generation.

![KMeans emotion space](E:/11.python%20work/cora-data/workflow/06_report_assets/05_kmeans_emotion_space.png)

![GMM text space](E:/11.python%20work/cora-data/workflow/06_report_assets/06_gmm_text_space.png)

![Cluster heatmap](E:/11.python%20work/cora-data/workflow/06_report_assets/07_category_cluster_heatmap.png)

---

## 1.5 Visualising and Plotting

Matplotlib and Seaborn were used to create analysis figures. The figures are
stored in:

`workflow/04_visualisation/outputs/`

Main outputs:

- dataset category counts
- TF-IDF vectorisation plot
- Hashing vectorisation plot
- image colour/texture PCA
- KMeans cluster plot
- GMM cluster plot
- category-cluster heatmap
- fragment parameter variation chart

![Fragment parameter variation](E:/11.python%20work/cora-data/workflow/06_report_assets/08_fragment_parameter_variation.png)

---

# Part 2: Design Tool Integration

## 2.1 Project Brief

The design tool workflow uses Python, Cinema 4D, and Processing.

Python is used for data processing, vectorisation, machine learning, and
fragment parameter generation. It translates the collected datasets into a CSV
of spatial rules.

Cinema 4D is used as the main 3D modelling and animation environment. It reads
the fragment parameter CSV and generates 32 architectural fragments with
different heights, colours, spacing logic, and animation keyframes.

Processing is used as a real-time animation and interaction environment. It
tests the emotional city logic through mouse-controlled emotion and density.
Moving the mouse left produces a relaxed/open park city; moving it right
produces a dense/stressful commercial city.

---

## 2.2 Integrated Workflows

## Workflow A: Data to Fragment Parameters

Pinterest images and OSM data are processed in Python. Image colour/texture
features and OSM text vectors are clustered. The cluster outputs are translated
into height, spacing, distortion, movement speed, colour, and scene position.

Output:

`workflow/05_design_tool_integration/fragment_parameters/emotion_city_fragments_32.csv`

## Workflow B: Fragment Parameters to Cinema 4D

Cinema 4D reads the fragment CSV and generates a 3D scene. Each fragment stores:

- source urban element
- emotional category
- KMeans cluster
- GMM cluster
- height, width, depth
- distortion
- movement speed
- RGB colour
- scene position

Cinema 4D script:

`workflow/05_design_tool_integration/cinema4d/generate_emotion_city_c4d.py`

## Workflow C: Emotion Rules to Processing

Processing uses the same emotional rules in an interactive sketch. The user
controls the emotional axis with the mouse:

- left = relaxed, open, park-like
- right = stressful, dense, commercial-like

Processing sketch:

`python_processing/python_processing.pde`

This sketch demonstrates the rule system live: height, spacing, distortion,
colour, pulse, and density all change continuously along the emotional axis.

---

## 2.3 Iterative Reconfiguration

The final fragment system contains 32 architectural fragments:

`workflow/05_design_tool_integration/fragment_parameters/emotion_city_fragments_32.csv`

Each fragment is generated through rule-based transformation. The fragments are
not manually modelled one by one. They are generated from machine-learning
cluster outputs and emotional design parameters.

Design rules:

- higher `value1` -> greater stress -> taller fragments
- higher `value2` -> greater density -> tighter spacing and larger mass
- KMeans cluster -> fragment variation group
- emotion category -> colour palette
- movement speed -> animation rhythm
- distortion -> spatial instability

The result is a systematic family of architectural fragments rather than
isolated objects.

---

## 2.4 3D Scenes and Animation

Cinema 4D animation:

`workflow/05_design_tool_integration/cinema4d/generate_emotion_city_c4d.py`

This script sets a 1800-frame animation at 30 fps, which equals 60 seconds. It
creates a scene with a ground plane, lights, camera movement, and 32 animated
fragments.

Processing animation:

`python_processing/python_processing.pde`

This sketch creates a real-time emotional city where the viewer can move
between relaxed/open and stressful/dense urban conditions.

Preview animation:

`workflow/06_report_assets/emotion_city_preview_65s.mp4`

This preview is 65 seconds long and was generated from the fragment CSV. It can
be used as a quick submission/crit preview while a higher-quality Cinema 4D
render is prepared.

---

# Project Conclusion

This project converts urban media and spatial datasets into an emotional
generation system. Images provide atmosphere, OSM data provides real urban
locations, vectorisation translates the datasets into feature spaces, machine
learning extracts cluster structures, and the design tools transform those
clusters into architectural fragments.

The project demonstrates a continuous workflow:

data collection -> vectorisation -> machine learning -> visual analysis ->
fragment rules -> Cinema 4D / Processing animation

The emotional city is therefore not only a visual metaphor. It is a design tool
where data-driven emotional categories directly produce spatial variation.

---

# Key File Index

Data:

- `photos1/`
- `photos2/`
- `metadata/pinterest_future_city_metadata.csv`
- `metadata/pinterest_business environment_metadata.csv`
- `workflow/01_data_collection/dataset4_openstreetmap_poi/outputs/openstreetmap_poi_dataset.csv`

Vectorisation:

- `workflow/02_vectorisation/scripts/run_emotion_city_pipeline.py`
- `workflow/02_vectorisation/outputs/text_vectorisation_tfidf_vs_hashing.csv`
- `workflow/02_vectorisation/outputs/image_vectorisation_colour_texture.csv`

Machine Learning:

- `workflow/03_machine_learning/outputs/osm_ml_clusters_kmeans_vs_gmm.csv`
- `workflow/03_machine_learning/outputs/ml_metrics.json`

Visualisation:

- `workflow/04_visualisation/outputs/`
- `workflow/06_report_assets/`

Design Tools:

- `workflow/05_design_tool_integration/fragment_parameters/emotion_city_fragments_32.csv`
- `workflow/05_design_tool_integration/cinema4d/generate_emotion_city_c4d.py`
- `python_processing/python_processing.pde`
- `workflow/05_design_tool_integration/processing/emotion_city_fragments_animation/emotion_city_fragments_animation.pde`

Animation:

- `workflow/06_report_assets/emotion_city_preview_65s.mp4`

---

# Submission Checklist

- Include final PDF report.
- Include GitHub repository link.
- Include datasets and scripts.
- Include OneDrive public folder for animation and 3D files.
- Remove all API keys before uploading.
- Do not upload `.env` files.
- Revoke any API key that was accidentally written in an old notebook.
