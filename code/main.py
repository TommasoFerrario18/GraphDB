from pyArango.connection import *
from nodes import *
from edges import *
from pyArango.graph import Graph, EdgeDefinition
from make_graph import SoulSyncGraph
import pandas as pd
from load_db import *

conn = Connection()

try:
    conn.createDatabase(name="SoulSync")
except CreationError:
    print("Couldn't create database, it probably already exists")
    pass

db = conn["SoulSync"]

try:
    db.createGraph("SoulSyncGraph")
except CreationError:
    print("Couldn't create graph, it probably already exist")
    pass

my_graph = db.graphs["SoulSyncGraph"]

users = pd.read_csv("./data/nodes.csv").drop(["Unnamed: 0"], axis=1)

# movie_genres = movie_genres(users)

# for genre in movie_genres:
#     my_graph.createVertex("MovieCategory", {"_key": genre, "name": genre})

# colors = users["favourite_color"].dropna().unique().tolist()
# for color in colors:
#     my_graph.createVertex("Color", {"_key": color, "name": color})

movies = users["favourite_movie"].dropna().unique().tolist()
for movie in movies:
    my_graph.createVertex("Movie", {"title": movie})
