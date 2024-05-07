from pyArango.connection import *
from nodes import *
from edges import *
from pyArango.graph import Graph, EdgeDefinition
from make_graph import SoulSyncGraph
import pandas as pd
from database import *
from insert import *


def fill_db(
    users: pd.DataFrame, edges: pd.DataFrame, matches: pd.DataFrame, graph, db: Database
):
    load_basic_nodes(users, graph, db)
    load_user_edges(edges, graph)
    load_country_city_edges(db, graph, users[["city", "country"]].drop_duplicates())
    load_matches(matches, graph)


db, my_graph = create_database()

users = pd.read_csv("./data/nodes.csv").drop(["Unnamed: 0"], axis=1)
edges = pd.read_csv("./data/edges.csv")
matches = pd.read_csv("./data/matches.csv")

# fill_db(users, edges, matches, my_graph, db)

# for collection in db.collections:
#     if collection[0] == "_":
#         continue
#     print(collection)

# ris = load_nodes_batch(users, db)
ris = {}

ris['countries_edge'] = load_country_city_edges_batches(db, users[["city", "country"]].drop_duplicates())
ris['Likes'] = load_user_edges_batch(edges, db)
ris['matches'] = load_matches_batch(matches, db)

print(ris)
