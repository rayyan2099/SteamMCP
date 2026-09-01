from pathlib import Path
import pickle

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATASETS_DIR = PROJECT_ROOT / "data" / "datasets"


def load_tag_data():
    """Load the tag recommender dataframe and normalized tag matrix."""

    with open(PROCESSED_DATA_DIR / "model_df.pkl", "rb") as file:
        model_df = pickle.load(file)

    tag_matrix = np.load(
        PROCESSED_DATA_DIR / "tag_matrix_normalized.npy"
    )

    return model_df, tag_matrix


def load_semantic_data():
    """Load semantic embeddings and their corresponding Steam app IDs."""

    appids = np.load(
        PROCESSED_DATA_DIR / "short_description_appids.npy"
    )

    embeddings = np.load(
        PROCESSED_DATA_DIR / "short_description_embeddings.npy"
    )

    return appids, embeddings


def load_description_data():
    """Load Steam game descriptions."""

    return pd.read_csv(
        DATASETS_DIR / "steam_descriptions_clean.csv"
    )


def load_games_data():
    """Load Steam game metadata."""

    return pd.read_csv(
        DATASETS_DIR / "steam_games_clean.csv"
    )