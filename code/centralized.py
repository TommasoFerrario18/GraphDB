from pyArango.connection import *
from nodes import *
from edges import *
from pyArango.graph import Graph, EdgeDefinition
from make_graph import SoulSyncGraph
from utils import *
import pandas as pd
from database import *

if __name__ == "__main__":
    nodes, edges, matches = read_all_csv()
    db, graph = create_database()

    print("Database created successfully")

    load_analysis_nodes(nodes, db, graph)

    print("Node Analysis loaded successfully")

    load_analysis_edges(edges, matches, db, graph)

    print("Edge Analysis loaded successfully")
