from pyArango.connection import *
from nodes import *
from edges import *
from pyArango.graph import Graph, EdgeDefinition
from make_graph import SoulSyncGraph
import pandas as pd
from database import *
from utils import *
from analysis import *
from insert import *


nodes, edges, matches = read_all_csv()
db, graph = create_database(
    arangoURL=["http://localhost:8000", "http://localhost:8001"],
    dbName="SoulSync",
    numberOfShards=3,
    replicationFactor=2,
    writeConcern=1,
)

# print("Database created successfully")

# load_analysis_nodes(nodes, db, graph, path="./results/loading_nodes_dist.csv")

# print("Analysis loaded successfully")

load_nodes_batch(nodes, db)

load_analysis_edges(edges, matches, db, graph, path="./results/loading_edges_dist.csv")

print("Edge Analysis loaded successfully")
