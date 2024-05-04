from pyArango.connection import *
from nodes import *
from edges import *
from pyArango.graph import Graph, EdgeDefinition
from make_graph import SoulSyncGraph
import pandas as pd
from database import *
from tqdm import tqdm


def read_all_csv():
    users = pd.read_csv("./data/nodes.csv").drop(["Unnamed: 0"], axis=1)
    edges = pd.read_csv("./data/edges.csv")
    matches = pd.read_csv("./data/matches.csv")
    return users, edges, matches


def load_analysis(users, edges, matches):
    results_df = pd.DataFrame(
        columns=[
            "city",
            "color",
            "country",
            # "likes",
            "located_in",
            # "matches",
            "movie",
            "movie_category",
            "user",
            "university"
        ]
    )

    for i in tqdm(range(10)):
        db, graph = create_db()
        row = {}
        row["movie_category"] = load_movie_genres(parse_movie_generes(users), graph)
        row["color"] = load_colors(
            users["favourite_color"].dropna().unique().tolist(), graph
        )
        row["movie"] = load_movies(
            users["favourite_movie"].dropna().unique().tolist(), graph
        )
        row["university"] = load_universities(
            users["university"].dropna().unique().tolist(), graph
        )
        row["country"] = load_countries(
            users.groupby(["country", "continent", "country_code"])
            .size()
            .reset_index()
            .drop_duplicates(),
            graph,
        )
        row["city"] = load_cities(parse_cities(users), graph)
        row["user"] = load_users(users, graph, db)
        # row["likes"] = load_user_edges(edges, graph)
        row["located_in"] = load_country_city_edges(
            db, graph, users[["city", "country"]].drop_duplicates()
        )
        # row["matches"] = load_matches(matches, graph)

        results_df = pd.concat([results_df, pd.Series(row).to_frame().T], ignore_index=True)

        drop_all(db)

    results_df.to_csv("./results/loading.csv")

def load_edges_analysis(users, edges, matches):
    results_df = pd.DataFrame(
        columns=[
            "likes",
            "matches",
        ]
    )
    
    qty = [10, 100, 1000, 10000, 50000, 100000, 200000]

    db, graph = create_db()
    # load_basic_nodes(users, graph, db)
    # load_country_city_edges(db, graph, users[["city", "country"]].drop_duplicates())
    
    for i in tqdm(range(len(qty))):    
        row = {}
        row["likes"] = load_user_edges(edges.head(qty[i]), graph)
        row["matches"] = load_matches(matches.head(qty[i]), graph)

        results_df = pd.concat([results_df, pd.Series(row).to_frame().T], ignore_index=True)
        
        db.collections["Likes"].truncate()
        db.collections["Matches"].truncate()
        
    results_df = results_df.set_index(pd.Index(qty))
        
    results_df.to_csv("./results/loading_edges.csv")

if __name__ == "__main__":
    # load_analysis(*read_all_csv())
    load_edges_analysis(*read_all_csv())
