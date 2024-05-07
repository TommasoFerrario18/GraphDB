from utils import *
from database import *
from insert import *
import itertools


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

    N = 10
    for i in tqdm(range(N)):
        for j in tqdm(range(len(qty)), leave=False):
            partial_nodes = nodes.head(qty[j])
            row = {}
            row["movie"], movies = load_movies_batch(
                partial_nodes["favourite_movie"].dropna().unique().tolist(), db
            )

            row["movie_category"] = load_movie_genres_batch(
                parse_movie_generes(partial_nodes), db
            )

            row["color"] = load_colors_batch(
                partial_nodes["favourite_color"].dropna().unique().tolist(), db
            )

            row["university"], uni = load_universities_batch(
                partial_nodes["university"].dropna().unique().tolist(), db
            )

            row["city"], cities = load_cities_batch(parse_cities(partial_nodes), db)

            row["country"] = load_countries_batch(
                partial_nodes.groupby(["country", "continent", "country_code"])
                .size()
                .reset_index()
                .drop_duplicates(),
                db,
            )

            row["user"] = load_users_batch(partial_nodes, db, movies, uni, cities)
            row["located_in"] = load_country_city_edges_batches(
                db, partial_nodes[["city", "country"]].drop_duplicates()
            )

            times_df = pd.concat(
                [times_df, pd.Series(row).to_frame().T], ignore_index=True
            )
            if i<N-1 or j<len(qty)-1:
                clear_all_collections(db)

    times_df = times_df.set_index(pd.Index(list(itertools.product(range(N), qty))))
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

    N = 10
    for i in tqdm(range(N)):
        for j in tqdm(range(len(qty)), leave=False):
            row = {}
            row["likes"] = load_user_edges_batch(edges.head(qty[j]), db)
            row["matches"] = load_matches_batch(matches.head(qty[j]), db)

            times_df = pd.concat(
                [times_df, pd.Series(row).to_frame().T], ignore_index=True
            )
            if i<N-1 or j<len(qty)-1:
                db.collections["Likes"].truncate()
                db.collections["Matches"].truncate()

    times_df = times_df.set_index(pd.Index(list(itertools.product(range(N), qty))))
    times_df.to_csv(path)
