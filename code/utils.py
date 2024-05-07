import pandas as pd


def parse_movie_generes(nodes: pd.DataFrame) -> list:
    """
    Parses the movie genres from the given DataFrame of nodes.

    Args:
        nodes (pd.DataFrame): DataFrame containing the nodes.

    Returns:
        list: List of unique movie genres.
    """
    rows = nodes["movie_genres"].apply(lambda x: x.split(","))
    rows = rows.apply(
        lambda x: [i.replace("[", "").replace("]", "").replace(" ", "") for i in x]
    )
    flat_list = [x for xs in rows.to_list() for x in xs]
    return pd.Series(flat_list).unique().tolist()


def read_all_csv() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Reads all the CSV files and returns them.
    """
    users = pd.read_csv("./data/nodes.csv").drop(["Unnamed: 0"], axis=1)
    edges = pd.read_csv("./data/edges.csv")
    matches = pd.read_csv("./data/matches.csv")
    return users, edges, matches
