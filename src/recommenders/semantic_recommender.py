import numpy as np
from sentence_transformers import SentenceTransformer

from src.utils.data_loader import (
    load_semantic_data,
    load_games_data
)
from src.utils.filters import filter_by_platform


# Load precomputed embeddings
semantic_appids, semantic_embeddings = load_semantic_data()

# Load game metadata
games_df = load_games_data()

# Don't load the model during module import
model = None


def get_model():
    """Load the embedding model only when semantic search is used."""

    global model

    if model is None:
        print(
            "Loading sentence transformer model...",
            flush=True
        )

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print(
            "Sentence transformer model loaded.",
            flush=True
        )

    return model


def semantic_search(query, top_n=10, platform=None):

    embedding_model = get_model()

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    )

    similarities = semantic_embeddings @ query_embedding

    results = games_df[
        games_df["appid"].isin(semantic_appids)
    ][["appid", "name", "platforms"]].copy()

    similarity_map = dict(
        zip(semantic_appids, similarities)
    )

    results["semantic_score"] = results[
        "appid"
    ].map(similarity_map)

    if platform:
        results = filter_by_platform(
            results,
            platform
        )

    results = results.sort_values(
        "semantic_score",
        ascending=False
    ).head(top_n)

    return results[
        ["name", "appid", "semantic_score"]
    ].reset_index(drop=True)
