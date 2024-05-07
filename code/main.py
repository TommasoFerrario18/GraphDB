from pyArango.connection import *
from nodes import *
from edges import *
from pyArango.graph import Graph, EdgeDefinition
from make_graph import SoulSyncGraph
from database import *
from insert import *
from analysis import *


def fill_database(db, nodes, edges, matches):
    load_nodes_batch(nodes, db)
    load_country_city_edges_batches(db, nodes[["city", "country"]].drop_duplicates())
    load_user_edges_batch(edges, db)
    load_matches_batch(matches, db)


typeDB = 0  # 0 for centralized, 1 for distributed
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
