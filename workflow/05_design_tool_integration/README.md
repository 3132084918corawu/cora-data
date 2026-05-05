# Design Tool Integration

The design tools use one shared fragment parameter file:

```text
fragment_parameters/emotion_city_fragments_32.csv
```

The fragments are generated from the Part 1 machine-learning outputs. Each
fragment stores category, emotion, cluster IDs, height, width, spacing,
distortion, movement speed, colour, and scene position.

## Workflow A: OSM + ML to Cinema 4D

`cinema4d/generate_emotion_city_c4d.py`

Cinema 4D reads the fragment CSV, creates 32 architectural blocks, scales and
rotates them from the emotional parameters, assigns category colours, and
keyframes a 60-second camera/fragment animation.

## Workflow B: OSM + ML to Processing

`processing/emotion_city_fragments_animation.pde`

Processing reads the same CSV from `processing/data/`, draws animated P3D
fragments, and uses movement speed/distortion to show relaxed versus stressful
urban rhythms.

## Workflow C: OSM + ML to Unreal

`unreal/generate_emotion_city_fragments_unreal.py`

Unreal can read the same CSV and spawn cube actors with category colours and
scale values. It is included as an optional third environment.

## Optional Blender Script

`blender/generate_emotion_city_fragments.py`

This is kept as an optional fallback, but the primary submitted 3D workflow is
Cinema 4D + Processing.
