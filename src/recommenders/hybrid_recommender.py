import pandas as pd

from src.recommenders.semantic_recommender import semantic_search
from src.recommenders.tag_recommender import find_games_by_tags


def hybrid_recommend(
    query,
    tags,
    platform=None,
    top_n=10,
    semantic_weight=0.3
):
    """
    Recommend games using both semantic search and tag matching.

    Parameters:
        query: Natural language description of the desired game.
        tags: List of Steam tags representing user preferences.
        platform: Optional platform filter (windows, mac, linux).
        top_n: Number of recommendations to return.
        semantic_weight: Weight given to semantic similarity.
                         Tag similarity gets the remaining weight.
    """

    tag_weight = 1 - semantic_weight

    # Get more candidates than needed so both recommenders
    # have enough results to contribute.
    candidate_count = top_n * 5

    semantic_results = semantic_search(
        query,
        top_n=candidate_count,
        platform=platform
    )

    tag_results = find_games_by_tags(
        tags,
        top_n=candidate_count,
        platform=platform
    )

    # Merge results using appid
    results = pd.merge(
        semantic_results,
        tag_results,
        on=["appid", "name"],
        how="outer"
    )

    # Games appearing in only one recommender get score 0
    results["semantic_score"] = results[
        "semantic_score"
    ].fillna(0)

    results["tag_score"] = results[
        "tag_score"
    ].fillna(0)

    # Normalize semantic scores
    max_semantic = results["semantic_score"].max()

    if max_semantic > 0:
        results["semantic_score_normalized"] = (
            results["semantic_score"] / max_semantic
        )
    else:
        results["semantic_score_normalized"] = 0

    # Normalize tag scores
    max_tag = results["tag_score"].max()

    if max_tag > 0:
        results["tag_score_normalized"] = (
            results["tag_score"] / max_tag
        )
    else:
        results["tag_score_normalized"] = 0

    # Calculate hybrid score
    results["hybrid_score"] = (
        semantic_weight
        * results["semantic_score_normalized"]
        +
        tag_weight
        * results["tag_score_normalized"]
    )

    # Sort by hybrid score
    results = results.sort_values(
        "hybrid_score",
        ascending=False
    )

    return results[
        [
            "name",
            "appid",
            "hybrid_score",
            "semantic_score",
            "tag_score"
        ]
    ].head(top_n).reset_index(drop=True)