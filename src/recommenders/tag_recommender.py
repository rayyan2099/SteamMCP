import numpy as np
import pandas as pd

from src.utils.data_loader import load_tag_data
from src.utils.filters import filter_by_platform


model_df, tag_matrix = load_tag_data()


def find_similar_by_tags(appid, top_n=10, platform=None):
    """
    Find games similar to a selected game using Steam tag similarity.

    Parameters:
        appid: Steam app ID of the selected game
        top_n: Number of recommendations to return
        platform: Optional platform filter (windows, mac, linux)
    """

    matches = model_df[model_df["appid"] == appid]

    if matches.empty:
        return {"error": f"Game not found with appid: {appid}"}

    game_index = matches.index[0]

    # Calculate similarity against every game
    similarities = tag_matrix @ tag_matrix[game_index]

    # Build results dataframe
    results = model_df[["name", "appid"]].copy()
    results["tag_score"] = similarities

    # Remove the selected game itself
    results = results[results["appid"] != appid]

    # Add platform information from the full games dataset
    from src.search.game_search import games_df

    results = results.merge(
        games_df[["appid", "platforms"]],
        on="appid",
        how="left"
    )

    # Apply platform filter if requested
    if platform:
        results = filter_by_platform(results, platform)

    # Sort and return top results
    results = results.sort_values(
        "tag_score",
        ascending=False
    ).head(top_n)

    return results[
        ["name", "appid", "tag_score"]
    ].reset_index(drop=True)

def find_games_by_tags(tags, top_n=10, platform=None):
    """
    Find games matching a list of Steam tags.

    Parameters:
        tags: List of tags to search for.
        top_n: Number of results to return.
        platform: Optional platform filter
                  (windows, mac, linux).
    """

    # Normalize user-provided tags
    tags = [
        tag.lower().strip().replace(" ", "_")
        for tag in tags
    ]

    # Keep only tags available in the dataset
    available_tags = [
        tag for tag in tags
        if tag in model_df.columns
    ]

    if not available_tags:
        return {
            "error": "None of the provided tags exist in the dataset."
        }

    # Get raw tag values
    tag_values = model_df[available_tags].astype(float)

    # Normalize each tag independently
    normalized_tags = (
        tag_values - tag_values.min()
    ) / (
        tag_values.max() - tag_values.min()
    )

    # Build results
    results = model_df[
        ["name", "appid"]
    ].copy()

    # Count how many requested tags each game matches
    results["matching_tags"] = (
        tag_values > 0
    ).sum(axis=1)

    # Average strength ONLY across tags the game actually has
    nonzero_scores = normalized_tags.where(tag_values > 0)

    results["tag_score"] = nonzero_scores.mean(axis=1)

    # Require at least 2 matching tags
    results = results[
        results["matching_tags"] >= 2
    ]

    # Add platform information
    from src.search.game_search import games_df

    results = results.merge(
        games_df[["appid", "platforms"]],
        on="appid",
        how="left"
    )

    # Apply platform filter
    if platform:
        results = filter_by_platform(
            results,
            platform
        )

    # Prioritize tag coverage, then match strength
    results = results.sort_values(
        ["matching_tags", "tag_score"],
        ascending=[False, False]
    )

    return results[
        ["name", "appid", "tag_score", "matching_tags"]
    ].head(top_n).reset_index(drop=True)