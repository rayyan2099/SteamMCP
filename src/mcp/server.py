from mcp.server.mcpserver import MCPServer
from src.search.game_search import search_games
from src.recommenders.tag_recommender import find_similar_by_tags
from src.recommenders.tag_recommender import (
    find_similar_by_tags,
    find_games_by_tags
)
from src.recommenders.hybrid_recommender import hybrid_recommend
from src.search.game_details import get_game_details

mcp = MCPServer("Steam Game Recommender")


@mcp.tool()
def search_for_games(query: str) -> list[dict]:
    """
    Search Steam games by name.

    Use this when the user mentions a game but you need to
    find the exact game first.
    """
    results = search_games(query)

    return results.to_dict(orient="records")

@mcp.tool()
def recommend_similar_games(
    appid: int,
    platform: str | None = None
) -> list[dict]:
    """
    Find games similar to a selected Steam game.

    Use this after the user has selected a game and you know
    its Steam appid.

    Optionally filter recommendations by platform:
    windows, mac, or linux.
    """
    results = find_similar_by_tags(
        appid,
        platform=platform
    )

    return results.to_dict(orient="records")

@mcp.tool()
def recommend_by_preferences(
    tags: list[str],
    platform: str | None = None
) -> list[dict]:
    """
    Recommend games based on gameplay preferences expressed as Steam tags.

    Use this when suitable tags are already known.

    Examples of tags:
    agriculture, relaxing, building, management, rpg,
    crafting, multiplayer, open_world, simulation.

    Optionally filter by platform: windows, mac, or linux.
    """
    results = find_games_by_tags(
        tags,
        platform=platform
    )

    return results.to_dict(orient="records")

@mcp.tool()
def recommend_hybrid(
    query: str,
    tags: list[str],
    platform: str | None = None
) -> list[dict]:
    """
    Recommend games using both natural language semantic search
    and explicit Steam tag preferences.

    Semantic similarity contributes 30% of the final score.
    Tag similarity contributes 70%.

    Optionally filter by platform: windows, mac, or linux.
    """

    results = hybrid_recommend(
        query=query,
        tags=tags,
        platform=platform
    )

    return results.to_dict(orient="records")

@mcp.tool()
def get_game_details_tool(appid: int) -> dict:
    """
    Get detailed information about a Steam game.

    Use this to retrieve a game's description, genres, tags,
    supported platforms, ratings, price, and other metadata.
    """
    return get_game_details(appid)


if __name__ == "__main__":
    import asyncio

    asyncio.run(mcp.run_stdio_async())
