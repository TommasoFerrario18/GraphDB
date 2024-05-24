from insert import *
from utils import *
from analysis import *
from query import *
from database import *

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
    fill_database(graph, nodes, edges, matches)

input("Press Enter to continue...")


# print("Ready to load nodes.")

# print("All data loaded.")

# input("Press Enter to continue...")
# print("Executing queries...")
# df = execute_all_queries("User/1", "US", db)
# print(df.mean())
# print(df.std())

# simulating_node_failure(graph, db, "1", "US", "1", 0.0, 0.0)

clear_all_collections(graph, db)
