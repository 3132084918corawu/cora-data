"""
Render a 65-second preview animation from the fragment CSV.

This is a lightweight preview render for the report folder. The higher-quality
3D version should be rendered from the Blender script in Part 2.
"""

from __future__ import annotations

import math
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FRAGMENTS = (
    ROOT
    / "workflow"
    / "05_design_tool_integration"
    / "fragment_parameters"
    / "emotion_city_fragments_32.csv"
)
OUT = ROOT / "workflow" / "06_report_assets" / "emotion_city_preview_65s.mp4"


def project(x: float, y: float, z: float, t: float) -> tuple[int, int]:
    angle = t * 0.18
    ca, sa = math.cos(angle), math.sin(angle)
    rx = x * ca - z * sa
    rz = x * sa + z * ca
    scale = 5.2 / (1 + (rz + 70) / 180)
    sx = int(640 + rx * scale)
    sy = int(460 - y * scale + rz * scale * 0.35)
    return sx, sy


def main() -> None:
    df = pd.read_csv(FRAGMENTS)
    fps = 15
    seconds = 65
    width, height = 1280, 720
    writer = cv2.VideoWriter(
        str(OUT),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    for frame in range(fps * seconds):
        t = frame / fps
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:, :] = (18, 16, 14)

        for grid in range(-60, 61, 10):
            p1 = project(grid, 0, -60, t)
            p2 = project(grid, 0, 60, t)
            p3 = project(-60, 0, grid, t)
            p4 = project(60, 0, grid, t)
            cv2.line(img, p1, p2, (45, 45, 45), 1)
            cv2.line(img, p3, p4, (45, 45, 45), 1)

        draw_rows = []
        for i, row in enumerate(df.itertuples(index=False)):
            pulse = math.sin(t * row.movement_speed + i * 0.7) * row.distortion
            draw_rows.append((row.scene_z, row, pulse))
        draw_rows.sort(key=lambda item: item[0])

        for i, (_, row, pulse) in enumerate(draw_rows):
            x, z = float(row.scene_x), float(row.scene_z)
            h = float(row.height) + pulse
            base = project(x, 0, z, t)
            top = project(x, h, z, t)
            w = max(4, int(float(row.width) * 3.5))
            color = (
                int(float(row.blue) * 255),
                int(float(row.green) * 255),
                int(float(row.red) * 255),
            )
            cv2.rectangle(
                img,
                (base[0] - w, top[1]),
                (base[0] + w, base[1]),
                color,
                thickness=-1,
            )
            cv2.rectangle(
                img,
                (base[0] - w, top[1]),
                (base[0] + w, base[1]),
                (230, 230, 230),
                thickness=1,
            )

        cv2.putText(
            img,
            "Emotion City Map - ML fragments / 65 second preview",
            (36, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (235, 235, 235),
            2,
            cv2.LINE_AA,
        )
        writer.write(img)

    writer.release()
    print(OUT)


if __name__ == "__main__":
    main()
