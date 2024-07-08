from database import *
from tqdm import tqdm
from insert import *
from utils import *
from query import *

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

    qty = [5_000, 10_000, 25_000, 50_000, 100_000]

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

            row["city"], cities = load_cities_batch(
                partial_nodes["city"].dropna().unique().tolist(), db
            )

            row["country"] = load_countries_batch(
                partial_nodes.groupby(["country", "continent", "country_code"])
                .size()
                .reset_index()
                .drop_duplicates(),
                db,
            )

            row["user"] = load_users_batch(partial_nodes, db, movies, uni, cities)

            df = partial_nodes[["country_code", "city"]].drop_duplicates()
            df = df.replace({"city": cities})
            row["located_in"] = load_country_city_edges_batches(db, df)

            times_df = pd.concat(
                [times_df, pd.Series(row).to_frame().T], ignore_index=True
            )
            if i < N - 1 or j < len(qty) - 1:
                clear_all_collections(graph, db)

    times_df = times_df.set_index(pd.Index(list(itertools.product(range(N), qty))))
    times_df.to_csv(path)


def load_analysis_edges(
    edges: pd.DataFrame,
    matches: pd.DataFrame,
    db,
    path="./results/loading_edges.csv",
):
    times_df = pd.DataFrame(
        columns=[
            "likes",
            "matches",
        ]
    )

    qty = [10_000, 50_000, 100_000, 250_000, 500_000, 1_000_000]

    N = 10
    for i in tqdm(range(N)):
        for j in tqdm(range(len(qty)), leave=False):
            row = {}
            row["likes"] = load_user_edges_batch(edges.head(qty[j]), db)
            row["matches"] = load_matches_batch(matches.head(qty[j]), db)

            times_df = pd.concat(
                [times_df, pd.Series(row).to_frame().T], ignore_index=True
            )
            if i < N - 1 or j < len(qty) - 1:
                db.collection("Likes").truncate()
                db.collection("Matches").truncate()

    times_df = times_df.set_index(pd.Index(list(itertools.product(range(N), qty))))
    times_df.to_csv(path)


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
            "Query_9",
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
        
        start = time.time()
        get_all_user(db)
        row["Query_9"] = time.time() - start

        times_df = pd.concat([times_df, pd.Series(row).to_frame().T], ignore_index=True)

    times_df = times_df.set_index(pd.Index(range(N)))
    return times_df
