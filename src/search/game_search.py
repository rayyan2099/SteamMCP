import pandas as pd

from src.utils.data_loader import PROCESSED_DATA_DIR


def load_game_metadata():
    """Load game metadata used for searching."""

    data_path = (
        PROCESSED_DATA_DIR.parent
        / "datasets"
        / "steam_games_clean.csv"
    )

    return pd.read_csv(data_path)


games_df = load_game_metadata()


def search_games(query, top_n=10):
    """
    Search for games by name.

    Returns games whose titles contain the search query.
    """

    query = query.lower().strip()

    matches = games_df[
        games_df["name"]
        .str.lower()
        .str.contains(query, na=False)
    ].copy()

    return matches[
        ["name", "appid", "platforms"]
    ].head(top_n)