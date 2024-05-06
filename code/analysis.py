from utils import *
from database import *

def load_analysis_nodes(
    nodes: pd.DataFrame, db, graph, path="./results/loading_nodes.csv"
):
    times_df = pd.DataFrame(
        columns=[
            "city",
            "color",
            "country",
            "located_in",
            "movie",
            "movie_category",
            "user",
            "university",
        ]
    )

    N = 1
    for i in tqdm(range(N)):
        row = {}
        row["movie_category"] = load_movie_genres(parse_movie_generes(nodes), graph)
        row["color"] = load_colors(
            nodes["favourite_color"].dropna().unique().tolist(), graph
        )
        row["movie"] = load_movies(
            nodes["favourite_movie"].dropna().unique().tolist(), graph
        )
        row["university"] = load_universities(
            nodes["university"].dropna().unique().tolist(), graph
        )
        row["country"] = load_countries(
            nodes.groupby(["country", "continent", "country_code"])
            .size()
            .reset_index()
            .drop_duplicates(),
            graph,
        )
        row["city"] = load_cities(parse_cities(nodes), graph)
        row["user"] = load_users(nodes, graph, db)
        row["located_in"] = load_country_city_edges(
            db, graph, nodes[["city", "country"]].drop_duplicates()
        )

        times_df = pd.concat([times_df, pd.Series(row).to_frame().T], ignore_index=True)
        if i != N - 1:
            clear_all_collections(db)

    times_df.to_csv(path)


def load_analysis_edges(
    edges: pd.DataFrame,
    matches: pd.DataFrame,
    db,
    graph,
    path="./results/loading_edges.csv",
):
    times_df = pd.DataFrame(
        columns=[
            "likes",
            "matches",
        ]
    )

    qty = [10, 100, 1000, 10000, 50000, 100000, 200000]

    for i in tqdm(range(1)):
        row = {}
        row["likes"] = load_user_edges(edges, graph)
        row["matches"] = load_matches(matches, graph)

        times_df = pd.concat([times_df, pd.Series(row).to_frame().T], ignore_index=True)

        db.collections["Likes"].truncate()
        db.collections["Matches"].truncate()

    times_df = times_df.set_index(pd.Index(qty))
    times_df.to_csv(path)