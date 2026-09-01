import pandas as pd

from src.utils.data_loader import load_games_data


games_df = load_games_data()

descriptions_df = pd.read_csv(
    "data/datasets/steam_descriptions_clean.csv"
)


def get_game_details(appid: int) -> dict:
    """
    Get detailed information about a Steam game using its appid.
    """

    game = games_df[
        games_df["appid"] == appid
    ]

    if game.empty:
        return {
            "error": f"Game with appid {appid} not found."
        }

    game = game.iloc[0]

    description = descriptions_df[
        descriptions_df["steam_appid"] == appid
    ]

    short_description = None
    detailed_description = None

    if not description.empty:
        description = description.iloc[0]

        short_description = description[
            "short_description"
        ]

        detailed_description = description[
            "detailed_description"
        ]

    return {
        "appid": int(game["appid"]),
        "name": game["name"],
        "release_date": game["release_date"],
        "developer": game["developer"],
        "publisher": game["publisher"],
        "platforms": game["platforms"],
        "categories": game["categories"],
        "genres": game["genres"],
        "steamspy_tags": game["steamspy_tags"],
        "price": float(game["price"]),
        "positive_ratings": int(game["positive_ratings"]),
        "negative_ratings": int(game["negative_ratings"]),
        "average_playtime": int(game["average_playtime"]),
        "short_description": short_description,
        "detailed_description": detailed_description
    }