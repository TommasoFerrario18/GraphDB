from arango import ArangoClient
from insert import *
from query import *
from tqdm import tqdm
from utils import *
from analysis import *


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


def clear_all_collections(graph, db):
    for collection in graph.vertex_collections():
        print(f"Deleting collection {collection}")
        db.collection(collection).truncate()

    for collection in graph.edge_definitions():
        print(f"Deleting collection {collection['edge_collection']}")
        db.collection(collection["edge_collection"]).truncate()


def create_database(typeDB):
    if typeDB == 0:
        client = ArangoClient(hosts="http://localhost:8529")
    elif typeDB == 1:
        client = ArangoClient(hosts=["http://localhost:8000", "http://localhost:8001"])

    sys_db = client.db("_system", username="", password="")

    if not sys_db.has_database("SoulSync"):
        if typeDB == 0:
            sys_db.create_database("SoulSync")
        elif typeDB == 1:
            sys_db.create_database("SoulSync")

    db = client.db("SoulSync", username="", password="")

    if db.has_graph("SoulSyncGraph"):
        graph = db.graph("SoulSyncGraph")
    else:
        if typeDB == 0:
            print("Creating centralized graph")
            graph = db.create_graph("SoulSyncGraph")
        elif typeDB == 1:
            graph = db.create_graph(
                "SoulSyncGraph",
                smart=True,
                shard_count=4,
                replication_factor=3,
                write_concern=2,
            )
        print("Graph created")
        create_collections(graph)

    print("Database setup completed.")
    return db, graph


def fill_database(graph, nodes, edges, matches):
    load_nodes_batch(nodes, graph)
    load_user_edges_batch(edges, graph)
    load_matches_batch(matches, graph)
