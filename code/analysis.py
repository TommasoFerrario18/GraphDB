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

    qty = [100, 500, 1_000, 5_000, 10_000]
    
    N = 1
    for i in tqdm(range(qty)):
        partial_nodes = nodes.head(qty[i])
        row = {}
        row["movie_category"] = load_movie_genres(parse_movie_generes(partial_nodes), graph)
        row["color"] = load_colors(
            partial_nodes["favourite_color"].dropna().unique().tolist(), graph
        )
        row["movie"] = load_movies(
            partial_nodes["favourite_movie"].dropna().unique().tolist(), graph
        )
        row["university"] = load_universities(
            partial_nodes["university"].dropna().unique().tolist(), graph
        )
        row["country"] = load_countries(
            partial_nodes.groupby(["country", "continent", "country_code"])
            .size()
            .reset_index()
            .drop_duplicates(),
            graph,
        )
        row["city"] = load_cities(parse_cities(partial_nodes), graph)
        row["user"] = load_users(partial_nodes, graph, db)
        row["located_in"] = load_country_city_edges(
            db, graph, partial_nodes[["city", "country"]].drop_duplicates()
        )

        times_df = pd.concat([times_df, pd.Series(row).to_frame().T], ignore_index=True)
        if i != len(qty) - 1:
            clear_all_collections(db)

    times_df = times_df.set_index(pd.Index(qty))
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

    qty = [1_000, 5_000, 10_000, 50_000, 100_000, 150_000]

    for i in tqdm(range(qty)):
        row = {}
        row["likes"] = load_user_edges(edges.head(qty[i]), graph)
        row["matches"] = load_matches(matches.head(qty[i]), graph)

        times_df = pd.concat([times_df, pd.Series(row).to_frame().T], ignore_index=True)

        db.collections["Likes"].truncate()
        db.collections["Matches"].truncate()

    times_df = times_df.set_index(pd.Index(qty))
    times_df.to_csv(path)