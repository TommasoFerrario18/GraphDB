import pandas as pd
from scipy import stats
from tqdm import tqdm
from database import *


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
        lambda x: [
            i.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
            for i in x
        ]
    )
    flat_list = [x for xs in rows.to_list() for x in xs]
    return pd.Series(flat_list).unique().tolist()


def parse_cities(nodes: pd.DataFrame) -> dict[str, pd.Series]:
    """
    Parses the cities from the given DataFrame of nodes.

    Args:
        nodes: DataFrame containing the nodes.

    Returns:
        dict: Dictionary where keys are cities and values are trimmed mean of lat and long.
    """
    cities = nodes["city"].unique().tolist()
    city_dict = {}
    for city in cities:
        city_info = nodes[nodes["city"] == city]
        city_info = city_info[["city", "lat", "long"]]

        city_dict[city] = city_info.groupby("city").apply(stats.trim_mean, 0.25)

    return city_dict


def read_all_csv():
    """
    Reads all the CSV files and returns them.
    """
    users = pd.read_csv("./data/nodes.csv").drop(["Unnamed: 0"], axis=1)
    edges = pd.read_csv("./data/edges.csv")
    matches = pd.read_csv("./data/matches.csv")
    return users, edges, matches


def clear_all_collections(db):
    """
    Clears all the collections in the database.
    """
    for collection in db.collections():
        if collection.name != "_graphs":
            collection.truncate()