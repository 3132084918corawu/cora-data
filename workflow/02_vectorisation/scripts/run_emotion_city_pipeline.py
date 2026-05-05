"""
Run the Emotion City Map analysis pipeline.

Outputs:
- text vectorisation: TF-IDF vs Hashing+SVD
- image vectorisation: colour histogram vs texture/edge features
- machine learning comparison: KMeans vs Gaussian Mixture
- visualisations with Matplotlib and Seaborn
- 3D fragment parameter CSV for Blender / Processing / Unreal
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer
from sklearn.metrics import adjusted_rand_score, classification_report, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / "workflow"
DATA4 = (
    WORKFLOW
    / "01_data_collection"
    / "dataset4_openstreetmap_poi"
    / "outputs"
    / "openstreetmap_poi_dataset.csv"
)
PHOTOS1 = ROOT / "photos1"
PHOTOS2 = ROOT / "photos2"

VEC_OUT = WORKFLOW / "02_vectorisation" / "outputs"
ML_OUT = WORKFLOW / "03_machine_learning" / "outputs"
VIS_OUT = WORKFLOW / "04_visualisation" / "outputs"
FRAG_OUT = WORKFLOW / "05_design_tool_integration" / "fragment_parameters"


def ensure_dirs() -> None:
    for path in (VEC_OUT, ML_OUT, VIS_OUT, FRAG_OUT):
        path.mkdir(parents=True, exist_ok=True)


def clean_text(value: object) -> str:
    text = "" if pd.isna(value) else str(value)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_osm_text_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA4)
    text_parts = [
        df["name"].map(clean_text),
        df["query_label"].map(clean_text),
        df["osm_key"].map(clean_text),
        df["osm_value"].map(clean_text),
        df["tags_json"].map(clean_text),
    ]
    df["text_for_vectorisation"] = (
        text_parts[0]
        + " "
        + text_parts[1]
        + " "
        + text_parts[2]
        + " "
        + text_parts[3]
        + " "
        + text_parts[4]
    )
    return df


def text_vectorisation(osm: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    texts = osm["text_for_vectorisation"].fillna("").tolist()
    labels = osm["category"].tolist()

    tfidf = TfidfVectorizer(max_features=120, stop_words="english", ngram_range=(1, 2))
    x_tfidf = tfidf.fit_transform(texts)
    svd_tfidf = TruncatedSVD(n_components=2, random_state=42)
    tfidf_2d = svd_tfidf.fit_transform(x_tfidf)

    hashing = HashingVectorizer(
        n_features=256,
        alternate_sign=False,
        stop_words="english",
        ngram_range=(1, 2),
    )
    x_hash = hashing.transform(texts)
    svd_hash = TruncatedSVD(n_components=2, random_state=42)
    hash_2d = svd_hash.fit_transform(x_hash)

    k_tfidf = KMeans(n_clusters=3, random_state=42, n_init=20).fit_predict(x_tfidf)
    k_hash = KMeans(n_clusters=3, random_state=42, n_init=20).fit_predict(x_hash)

    metrics = {
        "tfidf_silhouette": float(silhouette_score(x_tfidf, k_tfidf)),
        "hashing_silhouette": float(silhouette_score(x_hash, k_hash)),
        "tfidf_hashing_cluster_ari": float(adjusted_rand_score(k_tfidf, k_hash)),
        "tfidf_explained_variance_2d": float(svd_tfidf.explained_variance_ratio_.sum()),
        "hashing_explained_variance_2d": float(svd_hash.explained_variance_ratio_.sum()),
    }

    rows = pd.DataFrame(
        {
            "element_id": osm["element_id"],
            "name": osm["name"],
            "category": labels,
            "query_label": osm["query_label"],
            "tfidf_x": tfidf_2d[:, 0],
            "tfidf_y": tfidf_2d[:, 1],
            "hash_x": hash_2d[:, 0],
            "hash_y": hash_2d[:, 1],
            "tfidf_kmeans_cluster": k_tfidf,
            "hashing_kmeans_cluster": k_hash,
        }
    )
    rows.to_csv(VEC_OUT / "text_vectorisation_tfidf_vs_hashing.csv", index=False)

    terms = np.array(tfidf.get_feature_names_out())
    top_rows = []
    for component_id, comp in enumerate(svd_tfidf.components_):
        idx = np.argsort(comp)[-12:][::-1]
        for term, weight in zip(terms[idx], comp[idx]):
            top_rows.append(
                {
                    "component": component_id,
                    "term": term,
                    "weight": float(weight),
                }
            )
    pd.DataFrame(top_rows).to_csv(VEC_OUT / "tfidf_svd_top_terms.csv", index=False)
    return rows, metrics


def image_paths() -> list[tuple[Path, str, str]]:
    paths: list[tuple[Path, str, str]] = []
    for path in sorted(PHOTOS1.glob("*.jpg")):
        paths.append((path, "park relaxed", "pinterest_park_images"))
    for path in sorted(PHOTOS2.glob("*.jpg")):
        paths.append((path, "commercial stressful", "pinterest_business_images"))
    return paths


def image_features(path: Path) -> dict[str, float] | None:
    try:
        image = Image.open(path).convert("RGB").resize((128, 128))
    except Exception:
        return None

    arr = np.asarray(image).astype(np.float32) / 255.0
    gray = cv2.cvtColor((arr * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor((arr * 255).astype(np.uint8), cv2.COLOR_RGB2HSV)

    hist_h = cv2.calcHist([hsv], [0], None, [12], [0, 180]).flatten()
    hist_s = cv2.calcHist([hsv], [1], None, [8], [0, 256]).flatten()
    hist_v = cv2.calcHist([hsv], [2], None, [8], [0, 256]).flatten()
    hist = np.concatenate([hist_h, hist_s, hist_v])
    hist = hist / max(hist.sum(), 1.0)

    edges = cv2.Canny(gray, 80, 160)
    lap = cv2.Laplacian(gray, cv2.CV_64F)

    data: dict[str, float] = {
        "red_mean": float(arr[:, :, 0].mean()),
        "green_mean": float(arr[:, :, 1].mean()),
        "blue_mean": float(arr[:, :, 2].mean()),
        "red_std": float(arr[:, :, 0].std()),
        "green_std": float(arr[:, :, 1].std()),
        "blue_std": float(arr[:, :, 2].std()),
        "brightness": float(gray.mean() / 255.0),
        "contrast": float(gray.std() / 255.0),
        "edge_density": float((edges > 0).mean()),
        "texture_variance": float(lap.var() / 10000.0),
    }
    for i, value in enumerate(hist):
        data[f"hsv_hist_{i:02d}"] = float(value)
    return data


def image_vectorisation() -> tuple[pd.DataFrame, dict[str, float]]:
    rows = []
    for path, category, dataset in image_paths():
        feats = image_features(path)
        if feats is None:
            continue
        rows.append(
            {
                "image_id": path.stem,
                "path": str(path),
                "category": category,
                "dataset": dataset,
                **feats,
            }
        )
    df = pd.DataFrame(rows)
    feature_cols = [c for c in df.columns if c.startswith(("red_", "green_", "blue_", "brightness", "contrast", "edge", "texture", "hsv_"))]

    colour_cols = [
        "red_mean",
        "green_mean",
        "blue_mean",
        "red_std",
        "green_std",
        "blue_std",
        "brightness",
        "contrast",
    ]
    texture_cols = ["edge_density", "texture_variance"]
    scaler = StandardScaler()
    x_all = scaler.fit_transform(df[feature_cols])
    x_colour = StandardScaler().fit_transform(df[colour_cols])
    x_texture = StandardScaler().fit_transform(df[colour_cols + texture_cols])

    pca = PCA(n_components=2, random_state=42)
    points = pca.fit_transform(x_all)
    df["image_pca_x"] = points[:, 0]
    df["image_pca_y"] = points[:, 1]
    df["colour_kmeans_cluster"] = KMeans(n_clusters=2, random_state=42, n_init=20).fit_predict(x_colour)
    df["texture_kmeans_cluster"] = KMeans(n_clusters=2, random_state=42, n_init=20).fit_predict(x_texture)

    metrics = {
        "valid_images": int(len(df)),
        "colour_silhouette": float(silhouette_score(x_colour, df["colour_kmeans_cluster"])),
        "texture_silhouette": float(silhouette_score(x_texture, df["texture_kmeans_cluster"])),
        "colour_texture_cluster_ari": float(
            adjusted_rand_score(df["colour_kmeans_cluster"], df["texture_kmeans_cluster"])
        ),
        "image_pca_explained_variance_2d": float(pca.explained_variance_ratio_.sum()),
    }
    df.to_csv(VEC_OUT / "image_vectorisation_colour_texture.csv", index=False)
    return df, metrics


def machine_learning(osm: pd.DataFrame, text_vec: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    ml_df = osm.merge(
        text_vec[
            [
                "element_id",
                "tfidf_x",
                "tfidf_y",
                "hash_x",
                "hash_y",
                "tfidf_kmeans_cluster",
            ]
        ],
        on="element_id",
        how="left",
    )
    feature_cols = ["value1", "value2", "tfidf_x", "tfidf_y", "hash_x", "hash_y"]
    x = ml_df[feature_cols].fillna(0).to_numpy()
    x_scaled = StandardScaler().fit_transform(x)

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=30)
    gmm = GaussianMixture(n_components=4, random_state=42)
    ml_df["kmeans_cluster"] = kmeans.fit_predict(x_scaled)
    ml_df["gmm_cluster"] = gmm.fit_predict(x_scaled)

    encoder = LabelEncoder()
    y = encoder.fit_transform(ml_df["category"])
    x_train, x_test, y_train, y_test = train_test_split(
        x_scaled, y, test_size=0.25, random_state=42, stratify=y
    )
    forest = RandomForestClassifier(n_estimators=120, random_state=42)
    forest.fit(x_train, y_train)
    y_pred = forest.predict(x_test)

    metrics: dict[str, object] = {
        "kmeans_silhouette": float(silhouette_score(x_scaled, ml_df["kmeans_cluster"])),
        "gmm_silhouette": float(silhouette_score(x_scaled, ml_df["gmm_cluster"])),
        "kmeans_gmm_cluster_ari": float(
            adjusted_rand_score(ml_df["kmeans_cluster"], ml_df["gmm_cluster"])
        ),
        "random_forest_report": classification_report(
            y_test, y_pred, target_names=encoder.classes_, output_dict=True
        ),
        "feature_columns": feature_cols,
    }

    ml_df.to_csv(ML_OUT / "osm_ml_clusters_kmeans_vs_gmm.csv", index=False)
    (ML_OUT / "ml_metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return ml_df, metrics


def create_fragments(ml_df: pd.DataFrame, n: int = 32) -> pd.DataFrame:
    sample = ml_df.sort_values(["category", "query_label", "name"]).head(max(n, 20)).copy()
    rows = []
    for i, row in enumerate(sample.itertuples(index=False), start=1):
        stress = float(row.value1)
        density = float(row.value2)
        angle = i * math.pi * 2 / len(sample)
        radius = 18 + density * 28
        rows.append(
            {
                "fragment_id": f"fragment_{i:02d}",
                "source_element_id": row.element_id,
                "source_name": row.name,
                "category": row.category,
                "emotion": row.emotion1,
                "spatial_condition": row.emotion2,
                "kmeans_cluster": int(row.kmeans_cluster),
                "gmm_cluster": int(row.gmm_cluster),
                "height": round(3 + stress * 28 + (int(row.kmeans_cluster) * 1.5), 3),
                "width": round(2.5 + density * 5.5, 3),
                "depth": round(2.5 + density * 5.5, 3),
                "spacing": round(10 - density * 6, 3),
                "distortion": round(0.5 + stress * 6, 3),
                "movement_speed": round(0.2 + stress * 2.2, 3),
                "rotation_speed": round(0.01 + density * 0.08, 3),
                "red": round(0.2 + stress * 0.8, 3),
                "green": round(0.75 - stress * 0.45, 3),
                "blue": round(0.9 - stress * 0.65, 3),
                "scene_x": round(math.cos(angle) * radius, 3),
                "scene_y": 0,
                "scene_z": round(math.sin(angle) * radius, 3),
                "latitude": row.latitude,
                "longitude": row.longitude,
            }
        )
    fragments = pd.DataFrame(rows)
    fragments.to_csv(FRAG_OUT / "emotion_city_fragments_32.csv", index=False)
    return fragments


def plots(osm: pd.DataFrame, text_vec: pd.DataFrame, image_df: pd.DataFrame, ml_df: pd.DataFrame, fragments: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(7, 4))
    sns.countplot(data=osm, x="category", hue="query_label")
    plt.title("Dataset 4 OSM POI Counts by Emotional Category")
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.savefig(VIS_OUT / "01_osm_category_query_counts.png", dpi=240)
    plt.close()

    plt.figure(figsize=(6, 5))
    sns.scatterplot(data=text_vec, x="tfidf_x", y="tfidf_y", hue="category", style="tfidf_kmeans_cluster", s=50)
    plt.title("Text Vectorisation: TF-IDF + SVD")
    plt.tight_layout()
    plt.savefig(VIS_OUT / "02_text_tfidf_svd_clusters.png", dpi=240)
    plt.close()

    plt.figure(figsize=(6, 5))
    sns.scatterplot(data=text_vec, x="hash_x", y="hash_y", hue="category", style="hashing_kmeans_cluster", s=50)
    plt.title("Text Vectorisation: Hashing + SVD")
    plt.tight_layout()
    plt.savefig(VIS_OUT / "03_text_hashing_svd_clusters.png", dpi=240)
    plt.close()

    plt.figure(figsize=(6, 5))
    sns.scatterplot(data=image_df, x="image_pca_x", y="image_pca_y", hue="category", style="texture_kmeans_cluster", s=42)
    plt.title("Image Vectorisation: Colour + Texture PCA")
    plt.tight_layout()
    plt.savefig(VIS_OUT / "04_image_colour_texture_pca.png", dpi=240)
    plt.close()

    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=ml_df, x="value1", y="value2", hue="kmeans_cluster", style="category", s=65, palette="tab10")
    plt.title("Machine Learning 1: KMeans on Emotion-Space Features")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(VIS_OUT / "05_kmeans_emotion_space.png", dpi=240)
    plt.close()

    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=ml_df, x="tfidf_x", y="tfidf_y", hue="gmm_cluster", style="category", s=55, palette="tab10")
    plt.title("Machine Learning 2: Gaussian Mixture Clusters")
    plt.tight_layout()
    plt.savefig(VIS_OUT / "06_gmm_text_space.png", dpi=240)
    plt.close()

    heat = pd.crosstab(ml_df["category"], ml_df["kmeans_cluster"])
    plt.figure(figsize=(6, 4))
    sns.heatmap(heat, annot=True, fmt="d", cmap="viridis")
    plt.title("Category vs KMeans Cluster Heatmap")
    plt.tight_layout()
    plt.savefig(VIS_OUT / "07_category_cluster_heatmap.png", dpi=240)
    plt.close()

    plt.figure(figsize=(8, 4))
    frag_params = fragments[["fragment_id", "height", "spacing", "distortion", "movement_speed"]].melt(
        id_vars="fragment_id", var_name="parameter", value_name="value"
    )
    sns.lineplot(data=frag_params, x="fragment_id", y="value", hue="parameter", marker="o")
    plt.xticks(rotation=90)
    plt.title("Generated Fragment Parameters")
    plt.tight_layout()
    plt.savefig(VIS_OUT / "08_fragment_parameter_variation.png", dpi=240)
    plt.close()


def write_summary(text_metrics: dict[str, float], image_metrics: dict[str, float], ml_metrics: dict[str, object], fragments: pd.DataFrame) -> None:
    summary = {
        "project": "Emotion City Map",
        "datasets_used": {
            "pinterest_park_images": 200,
            "pinterest_business_images": 200,
            "openstreetmap_poi": int(pd.read_csv(DATA4).shape[0]),
            "google_maps_reviews": "collector prepared; requires GOOGLE_MAPS_API_KEY to collect 200-300 real reviews",
        },
        "vectorisation_comparison": {
            "text": "TF-IDF+SVD compared with HashingVectorizer+SVD on OSM POI text/tags.",
            "image": "Colour statistics/histograms compared with colour+texture edge features.",
            **text_metrics,
            **image_metrics,
        },
        "machine_learning_comparison": {
            "model_1": "KMeans clustering",
            "model_2": "Gaussian Mixture clustering",
            "classifier_check": "RandomForest predicts emotional category from vector/parameter features.",
            "kmeans_silhouette": ml_metrics["kmeans_silhouette"],
            "gmm_silhouette": ml_metrics["gmm_silhouette"],
            "kmeans_gmm_cluster_ari": ml_metrics["kmeans_gmm_cluster_ari"],
        },
        "design_outputs": {
            "fragment_count": int(len(fragments)),
            "fragment_parameters_csv": str(FRAG_OUT / "emotion_city_fragments_32.csv"),
        },
    }
    (WORKFLOW / "06_report_assets" / "workflow_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main() -> None:
    ensure_dirs()
    osm = load_osm_text_dataset()
    text_vec, text_metrics = text_vectorisation(osm)
    image_df, image_metrics = image_vectorisation()
    ml_df, ml_metrics = machine_learning(osm, text_vec)
    fragments = create_fragments(ml_df, n=32)
    plots(osm, text_vec, image_df, ml_df, fragments)
    write_summary(text_metrics, image_metrics, ml_metrics, fragments)
    print("Emotion City pipeline complete.")
    print(f"Text vectorisation rows: {len(text_vec)}")
    print(f"Valid image rows: {len(image_df)}")
    print(f"ML rows: {len(ml_df)}")
    print(f"Fragments: {len(fragments)}")


if __name__ == "__main__":
    main()
