BARC0074:

Bartlett Architecture Skills Portfolio

**Final Assignment Report**

Tutor: Loana Drogeanu

Student Number:25138105

**GitHub Repository:** [https://github.com/3132084918corawu/cora-data](https://github.com/3132084918corawu/cora-data)

**OneDrive Large Files:** [Emotion City Map public OneDrive folder](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx)

**Public Access Links (replace placeholders after upload):**

- [GitHub repository root](https://github.com/3132084918corawu/cora-data)
- [Workflow source code folder](https://github.com/3132084918corawu/cora-data/tree/main/workflow)
- [Dataset 1: Pinterest park images - OneDrive](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx)
- [Dataset 2: Pinterest commercial images - OneDrive](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx)
- [Dataset 3: Google Maps review outputs - OneDrive](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx)
- [Dataset 4: OpenStreetMap POI CSV - GitHub](https://github.com/3132084918corawu/cora-data/blob/main/workflow/01_data_collection/dataset4_openstreetmap_poi/outputs/openstreetmap_poi_dataset.csv)
- [Design tool files: Cinema 4D + Processing - OneDrive](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx)
- [Animation output: 65-second preview MP4 - OneDrive](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx)


Project Status

Goal

This project transforms machine-learning outputs, including vector
embeddings, clusters, and emotional parameters, into design-driving
systems for spatial generation. The project asks how a city can be read
as an emotional field. Parks are interpreted as relaxed and open,
commercial areas as stressful and dense, and transport nodes as tense
and fast.

The final design outcome is an emotional city generator. Each emotional
condition becomes a spatial rule:

Relaxed / open: lower height, wider spacing, slower movement, blue-green
tone.

Stressful / dense: taller height, tighter spacing, faster movement,
red-orange tone.

Tense / fast: directional movement, transitional rhythm, compressed
corridors.

The workflow links data collection, vectorisation, machine learning,
visualisation, and 3D generation. The data does not remain as analysis
only. It is translated into 32 architectural fragments and animated as a
one-minute spatial system.

Part 1: Projecting Between Domains

1.1 Web Scraping and Data Collection

The project uses three main datasets from two different domains:
Pinterest image data and OpenStreetMap urban point data. A Google Maps
review collector is also prepared as an optional extension that can be
run with an API key.

Dataset 1: Park / Relaxed Image Dataset

Source: Pinterest\
Domain: image / social media image search

Notebook: [Cinema 4D animation script](https://github.com/3132084918corawu/cora-data/blob/main/workflow/05_design_tool_integration/cinema4d/generate_emotion_city_c4d.py) [Fragment rules CSV](https://github.com/3132084918corawu/cora-data/blob/main/workflow/05_design_tool_integration/fragment_parameters/emotion_city_fragments_32.csv) [Processing emotion city sketch](https://github.com/3132084918corawu/cora-data/blob/main/python_processing/python_processing.pde) [Cinema 4D generator script](https://github.com/3132084918corawu/cora-data/blob/main/workflow/05_design_tool_integration/cinema4d/generate_emotion_city_c4d.py) [Fragment parameter generator pipeline](https://github.com/3132084918corawu/cora-data/blob/main/workflow/02_vectorisation/scripts/run_emotion_city_pipeline.py) [Design integration README](https://github.com/3132084918corawu/cora-data/blob/main/workflow/05_design_tool_integration/README.md) [Visualisation pipeline](https://github.com/3132084918corawu/cora-data/blob/main/workflow/02_vectorisation/scripts/run_emotion_city_pipeline.py) [Machine learning pipeline](https://github.com/3132084918corawu/cora-data/blob/main/workflow/02_vectorisation/scripts/run_emotion_city_pipeline.py) [OpenAI API synthetic text script](https://github.com/3132084918corawu/cora-data/blob/main/workflow/01_data_collection/dataset5_api_synthetic_emotion_text/scripts/generate_emotion_text_api.py) [Image vectorisation pipeline](https://github.com/3132084918corawu/cora-data/blob/main/workflow/02_vectorisation/scripts/run_emotion_city_pipeline.py) [Text vectorisation pipeline](https://github.com/3132084918corawu/cora-data/blob/main/workflow/02_vectorisation/scripts/run_emotion_city_pipeline.py) [Google Maps reviews collector](https://github.com/3132084918corawu/cora-data/blob/main/workflow/01_data_collection/dataset3_google_maps_reviews/scripts/collect_google_maps_reviews.py) [OpenStreetMap POI collector](https://github.com/3132084918corawu/cora-data/blob/main/workflow/01_data_collection/dataset4_openstreetmap_poi/scripts/collect_openstreetmap_poi.py) [Pinterest commercial scraping notebook](https://github.com/3132084918corawu/cora-data/blob/main/python%20final.ipynb) [Pinterest park scraping notebook](https://github.com/3132084918corawu/cora-data/blob/main/python%20final.ipynb)

Outputs: [65-second preview MP4 - OneDrive](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx) / [Preview render script](https://github.com/3132084918corawu/cora-data/blob/main/workflow/06_report_assets/render_emotion_city_preview.py) [32 fragment parameter CSV](https://github.com/3132084918corawu/cora-data/blob/main/workflow/05_design_tool_integration/fragment_parameters/emotion_city_fragments_32.csv) / [Fragment preview figure](https://github.com/3132084918corawu/cora-data/blob/main/workflow/04_visualisation/outputs/08_fragment_parameter_variation.png) [Processing sketch folder](https://github.com/3132084918corawu/cora-data/tree/main/python_processing) / [Processing animation files - OneDrive](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx) [Cinema 4D Python script](https://github.com/3132084918corawu/cora-data/blob/main/workflow/05_design_tool_integration/cinema4d/generate_emotion_city_c4d.py) / [C4D scene and renders - OneDrive](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx) [Fragment parameters CSV](https://github.com/3132084918corawu/cora-data/blob/main/workflow/05_design_tool_integration/fragment_parameters/emotion_city_fragments_32.csv) [Design integration folder](https://github.com/3132084918corawu/cora-data/tree/main/workflow/05_design_tool_integration) / [OneDrive large files folder](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx) [Matplotlib/Seaborn figure folder](https://github.com/3132084918corawu/cora-data/tree/main/workflow/04_visualisation/outputs) / [Report assets folder](https://github.com/3132084918corawu/cora-data/tree/main/workflow/06_report_assets) [KMeans vs GMM cluster CSV](https://github.com/3132084918corawu/cora-data/blob/main/workflow/03_machine_learning/outputs/osm_ml_clusters_kmeans_vs_gmm.csv) / [Metrics JSON](https://github.com/3132084918corawu/cora-data/blob/main/workflow/03_machine_learning/outputs/ml_metrics.json) [API synthetic emotion text folder](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx) [Image colour/texture CSV](https://github.com/3132084918corawu/cora-data/blob/main/workflow/02_vectorisation/outputs/image_vectorisation_colour_texture.csv) / [Image PCA figure](https://github.com/3132084918corawu/cora-data/blob/main/workflow/04_visualisation/outputs/04_image_colour_texture_pca.png) [TF-IDF vs Hashing CSV](https://github.com/3132084918corawu/cora-data/blob/main/workflow/02_vectorisation/outputs/text_vectorisation_tfidf_vs_hashing.csv) / [Top terms CSV](https://github.com/3132084918corawu/cora-data/blob/main/workflow/02_vectorisation/outputs/tfidf_svd_top_terms.csv) [Google reviews dataset output folder](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx) / [Validator script](https://github.com/3132084918corawu/cora-data/blob/main/workflow/01_data_collection/dataset3_google_maps_reviews/scripts/validate_google_maps_reviews.py) [OSM POI dataset CSV](https://github.com/3132084918corawu/cora-data/blob/main/workflow/01_data_collection/dataset4_openstreetmap_poi/outputs/openstreetmap_poi_dataset.csv) / [Raw OSM JSON folder](https://github.com/3132084918corawu/cora-data/tree/main/workflow/01_data_collection/dataset4_openstreetmap_poi/outputs/raw) [Commercial image folder - OneDrive](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx) / [Metadata CSV - GitHub](https://github.com/3132084918corawu/cora-data/blob/main/metadata/pinterest_business%20environment_metadata.csv) [Park image folder - OneDrive](https://1drv.ms/f/c/c3f06c7d124c9408/IgCKLY6JYjllQp8P0HdAEaB2Af9D9yTJIpSRN5HUIchQ_P4?e=gszafx) / [Metadata CSV - GitHub](https://github.com/3132084918corawu/cora-data/blob/main/metadata/pinterest_future_city_metadata.csv)

Collected elements: 200 image files\
Readable images used in analysis: 188

This dataset represents relaxed and open urban atmospheres. It contains
park, garden, landscape, and green-space references. In the design
logic, these images support the low-density, slow-moving, open spatial
condition.

![](workflow\06_report_assets\extracted_media_from_word/media/image1.png){width="5.768055555555556in"
height="3.2868055555555555in"}

Dataset 2: Commercial / Stressful Image Dataset

Source: Pinterest\
Domain: image / social media image search

Notebook:

Outputs:

Collected elements: 200 image files\
Readable images used in analysis: 199

This dataset represents dense commercial atmospheres. It includes
business environments, shopping areas, office-like environments, and
visually busier urban references. In the design logic, these images
support the high-density, compressed, vertical, and fast-moving
condition.

![](workflow\06_report_assets\extracted_media_from_word/media/image2.png){width="5.768055555555556in"
height="3.3340277777777776in"}

Dataset 3: OpenStreetMap Urban POI Dataset

Source: OpenStreetMap / Overpass API

Notebook:

Outputs:

Collected elements: 500

Category distribution:

park relaxed: 280

commercial stressful: 220

The OpenStreetMap dataset contains real urban elements with names, tags,
coordinates, and category labels. It gives the project a spatial anchor:
instead of only using atmosphere images, the system also works with
actual city locations such as parks, gardens, shops, and offices.

![](workflow\06_report_assets\extracted_media_from_word/media/image3.png){width="5.768055555555556in"
height="2.1590277777777778in"}

Google Maps Review Extension:

Notebook:

Outputs:

It is prepared to collect 200-300 real review records using the Google
Places API, but it requires GOOGLE_MAPS_API_KEY. Since no key was
available in this environment, the review dataset is documented as a
prepared extension rather than used as a generated result.

![](workflow\06_report_assets\extracted_media_from_word/media/image4.png){width="5.768055555555556in"
height="3.51875in"}

1.2 Dataset Vectorisation

Vectorisation was used to translate both image and text/spatial datasets
into machine-readable feature spaces.

Text / POI Vectorisation

Input dataset: OpenStreetMap POI names and tags

Notebook:

Outputs:

**Two vectorisation methods were compared:**

TF-IDF + SVD

HashingVectorizer + SVD

TF-IDF was selected because it is interpretable. It allows the report to
connect words and OSM tags such as park, garden, shop, and office back
to design decisions. This is useful for a design workflow because the
features are not a black box.

HashingVectorizer was selected as a comparison because it is faster and
more scalable. It does not store a vocabulary, so it is less readable,
but it can process larger streams of text with a fixed feature size.

**Result:**

TF-IDF silhouette: 0.235

Hashing silhouette: 0.109

Cluster agreement between both methods: ARI 0.490

**Interpretation:**

TF-IDF performed better for this dataset. OSM tags are short and
structured, so the vocabulary itself is meaningful. Hashing was faster
but less interpretable and produced weaker separation.

![](workflow\06_report_assets\extracted_media_from_word/media/image5.png){width="5.513043525809274in"
height="4.594425853018373in"}

*TF-IDF clusters*

![](workflow\06_report_assets\extracted_media_from_word/media/image6.png){width="5.13043416447944in"
height="4.275567585301837in"}

*Hashing clusters*

Image Vectorisation

Input datasets: Pinterest park images and Pinterest business images

Notebook:

Outputs:

![](workflow\06_report_assets\extracted_media_from_word/media/image7.png){width="5.768055555555556in"
height="2.589583333333333in"}

**Two image vectorisation strategies were compared:**

1.Colour statistics and HSV histograms

2.Colour + texture / edge features

Colour features were selected because the emotional contrast between
park and commercial atmospheres is partly visual: parks tend to contain
green-blue, softer, and more open images; commercial environments tend
to contain stronger contrast, hard surfaces, signage, glass, and
artificial lighting.

Texture and edge features were added as a comparison because commercial
spaces often have more hard boundaries, visual clutter, and sharper
geometry.

**Result:**

Valid images: 387

Colour feature silhouette: 0.306

Colour + texture feature silhouette: 0.251

Cluster agreement: ARI 0.822

**Interpretation:**

Colour separated the datasets more strongly than texture. Texture added
detail, but also noise, because some park images include paths,
buildings, and hard edges, while some commercial images have smooth
surfaces.

![](workflow\06_report_assets\extracted_media_from_word/media/image8.png){width="5.768055555555556in"
height="4.8069444444444445in"}

*Image PCA*

1.3 API Interaction for Structured Data Retrieval

The API interaction component is prepared in:

Notebook:

Outputs:

This script uses the OpenAI API to generate structured emotional city
observations. **Each generated item includes:**

sensory observation

emotional interpretation

spatial rule

keywords

The script is designed to augment the scraped and spatial datasets. It
creates text that directly connects emotion to spatial grammar, for
example:

**relaxed park atmosphere -\> horizontal expansion, wide spacing, slow
rhythm**

**stressful commercial atmosphere -\> vertical pressure, dense grid,
fast rhythm**

**tense transport atmosphere -\> directional corridors and compressed
waiting**

1.4 Machine Learning

Two machine-learning models were trained and compared using the OSM POI
dataset and vectorised features.

Notebook:

Outputs:

**Feature columns:**

value1

value2

TF-IDF SVD x/y

Hashing SVD x/y

Model 1: KMeans Clustering

KMeans was used to group urban elements into emotion-space clusters. It
is suitable for this project because the design system needs clear
cluster labels that can be mapped into spatial rules.

**Result:**

KMeans silhouette: 0.635

Model 2: Gaussian Mixture Model

Gaussian Mixture Model was used as a softer clustering comparison.
Unlike KMeans, GMM assumes data can belong to probabilistic
distributions. This is conceptually useful for emotional ambiguity,
where a place might be partly calm and partly stressful.

**Result:**

GMM silhouette: 0.494

**Comparison:**

KMeans performed better in this dataset because the emotional parameters
were clearly separated: relaxed/open elements have low value1/value2,
while commercial/stressful elements have high value1/value2. GMM is
still valuable as a design idea because it supports transitional
emotional zones, but KMeans produced cleaner clusters for direct
fragment generation.

![](workflow\06_report_assets\extracted_media_from_word/media/image9.png){width="5.768055555555556in"
height="4.120138888888889in"}

*KMeans emotion space*

![](workflow\06_report_assets\extracted_media_from_word/media/image10.png){width="5.768055555555556in"
height="4.120138888888889in"}

*GMM text space*

![](workflow\06_report_assets\extracted_media_from_word/media/image11.png){width="5.768055555555556in"
height="3.845138888888889in"}

*Cluster heatmap*

1.5 Visualising and Plotting

Matplotlib and Seaborn were used to create analysis figures.

The figures are stored in:

Notebook:

Outputs:

**Main outputs:**

dataset category counts

TF-IDF vectorisation plot

Hashing vectorisation plot

image colour/texture PCA

KMeans cluster plot

GMM cluster plot

category-cluster heatmap

fragment parameter variation chart

![](workflow\06_report_assets\extracted_media_from_word/media/image12.png){width="5.768055555555556in"
height="2.884027777777778in"}

*Fragment parameter variation*

Part 2: Design Tool Integration

2.1 Project Brief

The design tool workflow uses Python, Cinema 4D, and Processing.

Python is used for data processing, vectorisation, machine learning, and
fragment parameter generation. It translates the collected datasets into
a CSV of spatial rules.

Cinema 4D is used as the main 3D modelling and animation environment. It
reads the fragment parameter CSV and generates 32 architectural
fragments with different heights, colours, spacing logic, and animation
keyframes.

Processing is used as a real-time animation and interaction environment.
It tests the emotional city logic through mouse-controlled emotion and
density. Moving the mouse left produces a relaxed/open park city; moving
it right produces a dense/stressful commercial city.

2.2 Integrated Workflows

Workflow A: Data to Fragment Parameters

Pinterest images and OSM data are processed in Python. Image
colour/texture features and OSM text vectors are clustered. The cluster
outputs are translated into height, spacing, distortion, movement speed,
colour, and scene position.

Notebook:

Outputs:

Workflow B: Fragment Parameters to Cinema 4D

Cinema 4D reads the fragment CSV and generates a 3D scene. Each fragment
stores:

source urban element

emotional category

KMeans cluster

GMM cluster

height, width, depth

distortion

movement speed

RGB colour

scene position

Cinema 4D script:

Notebook:

Outputs:

Workflow C: Emotion Rules to Processing

Processing uses the same emotional rules in an interactive sketch. The
user controls the emotional axis with the mouse:

left = relaxed, open, park-like

right = stressful, dense, commercial-like

Notebook:

Outputs:

This sketch demonstrates the rule system live: height, spacing,
distortion, colour, pulse, and density all change continuously along the
emotional axis.

2.3 Iterative Reconfiguration

The final fragment system contains 32 architectural fragments:

Notebook:

Outputs:

Each fragment is generated through rule-based transformation. The
fragments are not manually modelled one by one. They are generated from
machine-learning cluster outputs and emotional design parameters.

Design rules:

higher value1 -\> greater stress -\> taller fragments

higher value2 -\> greater density -\> tighter spacing and larger mass

KMeans cluster -\> fragment variation group

emotion category -\> colour palette

movement speed -\> animation rhythm

distortion -\> spatial instability

The result is a systematic family of architectural fragments rather than
isolated objects.

2.4 3D Scenes and Animation

Cinema 4D animation:

Notebook:

Outputs:

This script sets a 1800-frame animation at 30 fps, which equals 60
seconds. It creates a scene with a ground plane, lights, camera
movement, and 32 animated fragments.

Processing animation :

python_processing/python_processing.pde

This sketch creates a real-time emotional city where the viewer can move
between relaxed/open and stressful/dense urban conditions.

Preview animation:

workflow/06_report_assets/emotion_city_preview_65s.mp4

This preview is 65 seconds long and was generated from the fragment CSV.
It can be used as a quick submission/crit preview while a higher-quality
Cinema 4D render is prepared.

Project Conclusion

This project converts urban media and spatial datasets into an emotional
generation system. Images provide atmosphere, OSM data provides real
urban locations, vectorisation translates the datasets into feature
spaces, machine learning extracts cluster structures, and the design
tools transform those clusters into architectural fragments.

The project demonstrates a continuous workflow:

data collection \-- vectorisation \-- machine learning \-- visual
analysis \-- fragment rules \-- Cinema 4D / Processing animation

The emotional city is therefore not only a visual metaphor. It is a
design tool where data-driven emotional categories directly produce
spatial variation.

