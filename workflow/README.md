# Emotional City Map Workflow

This folder organises the project pipeline from data collection to 3D scene
generation.

## Folder Structure

- `01_data_collection/` stores scraped and API-based datasets.
- `02_vectorisation/` is for TF-IDF, Doc2Vec, CLIP, ResNet, or embedding outputs.
- `03_machine_learning/` is for clustering, SOM, classification, and model results.
- `04_visualisation/` is for Matplotlib and Seaborn analysis figures.
- `05_design_tool_integration/` is for Processing, Blender, Unreal, or other design
  tool scripts and scene files.
- `06_report_assets/` is for selected images, diagrams, and final report material.

## Current Dataset 3

`01_data_collection/dataset3_google_maps_reviews/` contains the Google Maps
reviews workflow. It collects urban review text and attaches emotional/spatial
parameters so the review dataset can drive later vectorisation, clustering, and
3D fragment generation.
