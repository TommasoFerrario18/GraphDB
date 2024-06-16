from insert import *
from utils import *
from analysis import *
from query import *
from database import *
import time

typeDB = 1  # 0 for centralized, 1 for distributed
analysis = 0  # 0 no analysis, 1 for analysis

nodes, edges, matches = read_all_csv()

if typeDB == 0:
    path_edges = "./results/loading_edges_cent.csv"
    path_nodes = "./results/loading_nodes_cent.csv"
elif typeDB == 1:
    path_edges = "./results/loading_edges_dist.csv"
    path_nodes = "./results/loading_nodes_dist.csv"

start = time.time()
db, graph = create_database(typeDB)
print("Time to create database: ", time.time() - start)

clear_all_collections(graph, db)


input("Press Enter to continue with insertion...")

if analysis == 1:
    print("Database created successfully")

    load_analysis_nodes(nodes, db, graph, path_nodes)

    print("Node Analysis loaded successfully")

    load_analysis_edges(edges, matches, db, path_edges)

    print("Edge Analysis loaded successfully")
elif analysis == 0:
    print("Database created successfully")
    fill_database(db, nodes, edges, matches)

input("Press Enter to continue with queries...")

print("Executing queries...")
df = execute_all_queries("User/100", "US", db)
print(df.mean().T)
print(df.std().T)

input("Press Enter to continue with updates...")
update_all_city(db)
update_all_like(db)
update_user_city_edge("User/0", "City/100", db)
replace_all_user_field("100", {"name": "John Doe", "age": 30}, db)

input("Press Enter to continue with removals...")

delete_user_py("User/100", db, graph)
delete_user_AQL("User/101", db)
delete_user_color_edge("User/102", db)

print("Users deleted successfully")
