from arango import ArangoClient
from insert import *
from query import *
from tqdm import tqdm


def read_all_csv() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Reads all the CSV files and returns them.
    """
    users = pd.read_csv("./data/nodes.csv").drop(["Unnamed: 0"], axis=1)
    edges = pd.read_csv("./data/edges.csv")
    matches = pd.read_csv("./data/matches.csv")
    return users, edges, matches


def execute_all_queries(user_id: str, country_code: str, db):
    times_df = pd.DataFrame(
        columns=[
            "Query_1",
            "Query_2",
            "Query_3",
            "Query_4",
            "Query_5",
            "Query_6",
            "Query_7",
            "Query_8",
        ]
    )
    N = 30
    for i in tqdm(range(N)):
        row = {}
        start = time.time()
        get_user_data(user_id, db)
        row["Query_1"] = time.time() - start

        start = time.time()
        get_users_which_like_user(user_id, db)
        row["Query_2"] = time.time() - start

        start = time.time()
        find_user_which_like_same_movie_category(user_id, db)
        row["Query_3"] = time.time() - start

        start = time.time()
        get_all_users_which_live_in_same_city(user_id, db)
        row["Query_4"] = time.time() - start

        start = time.time()
        get_users_which_have_same_movie_and_studied_same_university(user_id, db)
        row["Query_5"] = time.time() - start

        start = time.time()
        get_likes_of_user_match(user_id, db)
        row["Query_6"] = time.time() - start

        start = time.time()
        get_all_user_of_a_country(country_code, db)
        row["Query_7"] = time.time() - start

        start = time.time()
        get_number_of_users_in_city(db)
        row["Query_8"] = time.time() - start

        times_df = pd.concat([times_df, pd.Series(row).to_frame().T], ignore_index=True)

    times_df = times_df.set_index(pd.Index(range(N)))
    return times_df


def create_collections(graph):
    graph.create_vertex_collection("User")
    graph.create_vertex_collection("Movie")
    graph.create_vertex_collection("MovieCategory")
    graph.create_vertex_collection("City")
    graph.create_vertex_collection("Country")
    graph.create_vertex_collection("Continent")
    graph.create_vertex_collection("University")
    graph.create_vertex_collection("Color")

    graph.create_edge_definition(
        edge_collection="Likes",
        from_vertex_collections=["User"],
        to_vertex_collections=["User"],
    )
    graph.create_edge_definition(
        edge_collection="Matches",
        from_vertex_collections=["User"],
        to_vertex_collections=["User"],
    )
    graph.create_edge_definition(
        edge_collection="IntMovie",
        from_vertex_collections=["User"],
        to_vertex_collections=["Movie"],
    )
    graph.create_edge_definition(
        edge_collection="IntColor",
        from_vertex_collections=["User"],
        to_vertex_collections=["Color"],
    )
    graph.create_edge_definition(
        edge_collection="IntMovieCategory",
        from_vertex_collections=["User"],
        to_vertex_collections=["MovieCategory"],
    )
    graph.create_edge_definition(
        edge_collection="LivesIn",
        from_vertex_collections=["User"],
        to_vertex_collections=["City"],
    )
    graph.create_edge_definition(
        edge_collection="LocatedIn",
        from_vertex_collections=["City"],
        to_vertex_collections=["Country"],
    )
    graph.create_edge_definition(
        edge_collection="StudiesAt",
        from_vertex_collections=["User"],
        to_vertex_collections=["University"],
    )
    graph.create_edge_definition(
        edge_collection="CountryLocatedIn",
        from_vertex_collections=["Country"],
        to_vertex_collections=["Continent"],
    )


client = ArangoClient(hosts="http://localhost:8529")

sys_db = client.db("_system", username="", password="")

if not sys_db.has_database("SoulSync"):
    sys_db.create_database("SoulSync")

db = client.db("SoulSync", username="", password="")

if db.has_graph("SoulSyncGraph"):
    graph = db.graph("SoulSyncGraph")
else:
    graph = db.create_graph("SoulSyncGraph")

    create_collections(graph)

print("Database setup completed.")
print(graph.vertex_collections())

nodes, edges, matches = read_all_csv()

# print("Ready to load nodes.")
# load_nodes_batch(nodes, graph)
# load_user_edges_batch(edges, graph)
# load_matches_batch(matches, graph)
# print("All data loaded.")

input("Press Enter to continue...")
print("Executing queries...")
df = execute_all_queries("User/1", "US", db)
print(df)