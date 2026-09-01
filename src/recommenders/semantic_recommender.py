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

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def semantic_search(query, top_n=10, platform=None):
    """
    Search for games using a natural language description.

    Parameters:
        query: Natural language game description
        top_n: Number of results to return
        platform: Optional platform filter
                  (windows, mac, linux)
    """

    # Convert user query into an embedding
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    # Calculate cosine similarity
    similarities = semantic_embeddings @ query_embedding

    # Create results using semantic appids
    results = games_df[
        games_df["appid"].isin(semantic_appids)
    ][["appid", "name", "platforms"]].copy()

    # Map appid -> similarity score
    similarity_map = dict(
        zip(semantic_appids, similarities)
    )

    results["semantic_score"] = results[
        "appid"
    ].map(similarity_map)

    # Apply platform filter
    if platform:
        results = filter_by_platform(
            results,
            platform
        )

    # Sort and return results
    results = results.sort_values(
        "semantic_score",
        ascending=False
    ).head(top_n)

    return results[
        ["name", "appid", "semantic_score"]
    ].reset_index(drop=True)