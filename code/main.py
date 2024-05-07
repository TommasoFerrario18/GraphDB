from pyArango.connection import *
from nodes import *
from edges import *
from pyArango.graph import Graph, EdgeDefinition
from make_graph import SoulSyncGraph
import pandas as pd
from database import *
from insert import *
from analysis import *

typeDB = 0 # 0 for centralized, 1 for distributed 

nodes, edges, matches = read_all_csv()

if typeDB == 0:
    path_edges = "./results/loading_edges_cent.csv"
    path_nodes = "./results/loading_nodes_cent.csv"
elif typeDB == 1:
    path_edges = "./results/loading_edges_dist.csv"
    path_nodes = "./results/loading_nodes_dist.csv"

db, graph = create_database(typeDB) 

print("Database created successfully")

load_analysis_nodes(nodes, db, graph, path_nodes)

print("Node Analysis loaded successfully")

load_analysis_edges(edges, matches, db, graph, path_edges)

print("Edge Analysis loaded successfully")
