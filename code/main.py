from pyArango.graph import Graph, EdgeDefinition
from make_graph import SoulSyncGraph
from pyArango.connection import *
from database import *
from analysis import *
from insert import *
from nodes import *
from edges import *

import pandas as pd


def fill_database(db, nodes, edges, matches):
    load_nodes_batch(nodes, db)
    load_user_edges_batch(edges, db)
    load_matches_batch(matches, db)


typeDB = 1  # 0 for centralized, 1 for distributed
analysis = 0  # 0 no analysis, 1 for analysis

nodes, edges, matches = read_all_csv()

if typeDB == 0:
    path_edges = "./results/loading_edges_cent.csv"
    path_nodes = "./results/loading_nodes_cent.csv"
elif typeDB == 1:
    path_edges = "./results/loading_edges_dist.csv"
    path_nodes = "./results/loading_nodes_dist.csv"

db, graph = create_database(typeDB)

if analysis == 1:
    print("Database created successfully")

    load_analysis_nodes(nodes, db, path_nodes)

    print("Node Analysis loaded successfully")

    load_analysis_edges(edges, matches, db, path_edges)

    print("Edge Analysis loaded successfully")
elif analysis == 0:
    print("Database created successfully")
    fill_database(db, nodes, edges, matches)

input("Press Enter to continue...")

df = execute_all_queries("User/1", "US", db)
# print(df)

# delete_user_py("User/1", db, graph)
# delete_user_AQL("User/2", db)

# update_city("100", -22.455980, -47.532410, db)

# replace_all_user_field(
#     "0",
#     {
#         "first_name": "Cristiano",
#         "last_name": "Ronaldo",
#         "email": "cr7@arstechnica.com",
#         "phone": "165-321-0452",
#         "birth_date": "11/10/1985",
#         "gender": "Male",
#         "latitude": -7.1927733,
#         "longitude": -48.204827,
#     }, db
# )
