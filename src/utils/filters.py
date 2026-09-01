def filter_by_platform(games_df, platform):
    """
    Filter games by supported platform.

    Example platforms:
    windows
    mac
    linux
    """

    if platform is None:
        return games_df

    platform = platform.lower()

    return games_df[
        games_df["platforms"]
        .fillna("")
        .str.lower()
        .str.split(";")
        .apply(lambda platforms: platform in platforms)
    ].copy()