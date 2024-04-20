import time
import pandas as pd
from utils import *
from pyArango.connection import *


# Create a database and all the collections and graphs needed
def create_db():
    # Create a connection to the database
    conn = Connection()

    # Create the database
    try:
        conn.createDatabase(name="SoulSync")
    except CreationError:
        print("Couldn't create database, it probably already exists")
        pass

    # Connect to the database
    db = conn["SoulSync"]

    # Create the graph
    try:
        db.createGraph("SoulSyncGraph")
    except CreationError:
        print("Couldn't create graph, it probably already exist")
        pass

    return db, db.graphs["SoulSyncGraph"]


# Load Data
def load_movies(movies: list, graph):
    print("Loading movies...\nSize: ", len(movies), "\n")
    start = time.time()
    for movie in movies:
        graph.createVertex("Movie", {"title": movie})
    end = time.time()
    print("Movies loaded in ", end - start, " seconds\n")


def load_movie_genres(movie_genres: list, graph):
    print("Loading movie genres...\nSize: ", len(movie_genres), "\n")
    start = time.time()
    for genre in movie_genres:
        graph.createVertex("MovieCategory", {"_key": genre, "name": genre})
    end = time.time()
    print("Movie genres loaded in ", end - start, " seconds\n")


def load_colors(colors: list, graph):
    print("Loading colors...\nSize: ", len(colors), "\n")
    start = time.time()
    for color in colors:
        graph.createVertex("Color", {"_key": color, "name": color})
    end = time.time()
    print("Colors loaded in ", end - start, " seconds\n")


def load_universities(universities: list, graph):
    print("Loading universities...\nSize: ", len(universities), "\n")
    start = time.time()
    for university in universities:
        graph.createVertex("University", {"name": university})
    end = time.time()
    print("Universities loaded in ", end - start, " seconds\n")


def load_cities(cities: dict, graph):
    print("Loading cities...\nSize: ", len(cities), "\n")
    start = time.time()
    for city in cities:
        city_info = cities[city]
        graph.createVertex(
            "City",
            {"name": city, "latitude": city_info[0][0], "longitude": city_info[0][1]},
        )
    end = time.time()
    print("Cities loaded in ", end - start, " seconds\n")


def load_countries(countries: pd.DataFrame, graph):
    print("Loading countries...\nSize: ", len(countries), "\n")
    start = time.time()
    for row in countries.iterrows():
        row = row[1]
        name = ["country"]
        code = row["country_code"]
        continent = row["continent"]
        graph.createVertex(
            "Country", {"name": name, "code": code, "continent": continent}
        )
    end = time.time()
    print("Countries loaded in ", end - start, " seconds\n")


def load_basic_nodes(nodes: pd.DataFrame, my_graph):
    load_movie_genres(parse_movie_generes(nodes), my_graph)
    load_colors(nodes["favourite_color"].dropna().unique().tolist(), my_graph)
    load_movies(nodes["favourite_movie"].dropna().unique().tolist(), my_graph)
    load_universities(nodes["university"].dropna().unique().tolist(), my_graph)
    load_countries(
        nodes.groupby(["country", "continent", "country_code"])
        .size()
        .reset_index()
        .drop_duplicates(),
        my_graph,
    )
    load_cities(parse_cities(nodes), my_graph)
