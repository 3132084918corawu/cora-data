"""
Unreal Python script: generate Emotion City fragments from CSV.

Use inside Unreal Editor with Python enabled. Update CSV_PATH if your project
folder differs. The script creates cube actors, scales them from the fragment
parameters, and applies emotion-based colours.
"""

from __future__ import annotations

import csv
from pathlib import Path

import unreal


CSV_PATH = Path(
    r"E:\11.python work\cora-data\workflow\05_design_tool_integration\fragment_parameters\emotion_city_fragments_32.csv"
)


def make_material(name: str, red: float, green: float, blue: float):
    material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name=name,
        package_path="/Game/EmotionCity/Materials",
        asset_class=unreal.Material,
        factory=unreal.MaterialFactoryNew(),
    )
    material.set_editor_property("diffuse_color", unreal.LinearColor(red, green, blue, 1.0))
    return material


def main():
    editor = unreal.EditorLevelLibrary
    materials = {}

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            category = row["category"].replace(" ", "_")
            mat_key = category
            if mat_key not in materials:
                materials[mat_key] = make_material(
                    f"M_{mat_key}",
                    float(row["red"]),
                    float(row["green"]),
                    float(row["blue"]),
                )

            location = unreal.Vector(
                float(row["scene_x"]) * 100,
                float(row["scene_z"]) * 100,
                float(row["height"]) * 50,
            )
            actor = editor.spawn_actor_from_class(unreal.StaticMeshActor, location)
            actor.set_actor_label(row["fragment_id"])
            mesh_component = actor.static_mesh_component
            cube = unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
            mesh_component.set_static_mesh(cube)
            actor.set_actor_scale3d(
                unreal.Vector(
                    float(row["width"]) * 0.45,
                    float(row["depth"]) * 0.45,
                    float(row["height"]) * 0.45,
                )
            )
            mesh_component.set_material(0, materials[mat_key])


main()
