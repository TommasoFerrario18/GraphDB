import time
import pandas as pd
from utils import *
from pyArango.connection import *
from concurrent.futures import ThreadPoolExecutor

batch_size = 100


def insert_batch(batch, collection):
    collection.bulkSave(batch)


def load_movies_batch(movies: list, db):
    print("Loading movies...\nSize: ", len(movies), "\n")
    docs = []
    new_movies = {}

    for id, movie in enumerate(movies):
        docs.append({"_key": str(id), "title": movie})
        new_movies[movie] = id

    batches = [docs[i : i + batch_size] for i in range(0, len(docs), batch_size)]

    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["Movie"]) for batch in batches
        ]
        for f in features:
            f.result()

    end = time.time()
    print("Movies loaded in ", end - start, " seconds\n")
    return end - start, new_movies


def load_movie_genres_batch(movie_genres: list, db):
    print("Loading movie genres...\nSize: ", len(movie_genres), "\n")

    docs = []
    for genre in movie_genres:
        if genre == "nan" or genre == "(nogenreslisted)":
            continue
        docs.append({"_key": genre, "name": genre})

    start = time.time()
    insert_batch(docs, db["MovieCategory"])
    end = time.time()
    print("Movie genres loaded in ", end - start, " seconds\n")
    return end - start


def load_colors_batch(colors: list, db):
    print("Loading colors...\nSize: ", len(colors), "\n")
    docs = []
    for color in colors:
        docs.append({"_key": color, "name": color})

    start = time.time()
    insert_batch(docs, db["Color"])
    end = time.time()
    print("Colors loaded in ", end - start, " seconds\n")
    return end - start


def load_universities_batch(universities: list, db):
    print("Loading universities...\nSize: ", len(universities), "\n")
    docs = []
    new_universities = {}
    for id, university in enumerate(universities):
        docs.append({"_key": str(id), "name": university})
        new_universities[university] = id

    batches = [docs[i : i + batch_size] for i in range(0, len(docs), batch_size)]

    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["University"]) for batch in batches
        ]
        for f in features:
            f.result()
    end = time.time()
    print("Universities loaded in ", end - start, " seconds\n")
    return end - start, new_universities


def load_cities_batch(cities: dict, db):
    print("Loading cities...\nSize: ", len(cities), "\n")

    new_cities = {}
    docs = []

    for id, city in enumerate(cities):
        docs.append({"_key": str(id), "name": city})
        new_cities[city] = id

    batches = [docs[i : i + batch_size] for i in range(0, len(docs), batch_size)]

    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["City"]) for batch in batches
        ]
        for f in features:
            f.result()
    end = time.time()
    print("Cities loaded in ", end - start, " seconds\n")
    return end - start, new_cities


def load_countries_batch(countries: pd.DataFrame, db):
    print("Loading countries...\nSize: ", len(countries), "\n")
    docs = []
    for row in countries.iterrows():
        row = row[1]
        docs.append(
            {
                "_key": row["country_code"],
                "name": row["country"],
                "code": row["country_code"],
                "continent": row["continent"],
            }
        )

    batches = [docs[i : i + batch_size] for i in range(0, len(docs), batch_size)]

    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["Country"]) for batch in batches
        ]
        for f in features:
            f.result()
    end = time.time()
    print("Countries loaded in ", end - start, " seconds\n")
    return end - start


def load_users_batch(
    nodes: pd.DataFrame, db, movies: dict, universities: dict, cities: dict
):
    print("Loading users...\nSize: ", len(nodes), "\n")

    user_docs = []
    movie_genres_docs = []
    movies_docs = []
    colors_docs = []
    universities_docs = []
    cities_docs = []

    for row in nodes.iterrows():
        id = row[0]
        row = row[1]
        user_docs.append(
            {
                "_key": str(id),
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "phone": row["phone"],
                "birth_date": row["birthDate"],
                "gender": row["gender"],
                "latitude": row["lat"],
                "longitude": row["long"],
            }
        )
        cities_docs.append(
            {"_from": "User/" + str(id), "_to": "City/" + str(cities[row["city"]])}
        )
        if not pd.isnull(row["university"]):
            universities_docs.append(
                {
                    "_from": "User/" + str(id),
                    "_to": "University/" + str(universities[row["university"]]),
                }
            )

        if not pd.isnull(row["favourite_movie"]):
            movies_docs.append(
                {
                    "_from": "User/" + str(id),
                    "_to": "Movie/" + str(movies[row["favourite_movie"]]),
                }
            )

        if not pd.isnull(row["favourite_color"]):
            colors_docs.append(
                {
                    "_from": "User/" + str(id),
                    "_to": "Color/" + str(row["favourite_color"]),
                }
            )

        if not pd.isnull(row["movie_genres"]):
            genres = row["movie_genres"].split(",")
            genres = list(
                map(
                    lambda x: x.replace("[", "").replace("]", "").replace(" ", ""),
                    genres,
                )
            )
            for genre in genres:
                movie_genres_docs.append(
                    {"_from": "User/" + str(id), "_to": "MovieCategory/" + str(genre)}
                )

    batches = [
        user_docs[i : i + batch_size] for i in range(0, len(user_docs), batch_size)
    ]
    movie_genres_batches = [
        movie_genres_docs[i : i + batch_size]
        for i in range(0, len(movie_genres_docs), batch_size)
    ]
    movies_batches = [
        movies_docs[i : i + batch_size] for i in range(0, len(movies_docs), batch_size)
    ]
    colors_batches = [
        colors_docs[i : i + batch_size] for i in range(0, len(colors_docs), batch_size)
    ]
    universities_batches = [
        universities_docs[i : i + batch_size]
        for i in range(0, len(universities_docs), batch_size)
    ]
    cities_batches = [
        cities_docs[i : i + batch_size] for i in range(0, len(cities_docs), batch_size)
    ]
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["User"]) for batch in batches
        ]
        for f in features:
            f.result()

    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["IntMovieCategory"])
            for batch in movie_genres_batches
        ]
        for f in features:
            f.result()

    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["IntMovie"])
            for batch in movies_batches
        ]
        for f in features:
            f.result()

    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["IntColor"])
            for batch in colors_batches
        ]
        for f in features:
            f.result()

    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["StudiesAt"])
            for batch in universities_batches
        ]
        for f in features:
            f.result()

    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["LivesIn"])
            for batch in cities_batches
        ]
        for f in features:
            f.result()

    end = time.time()
    print("Users loaded in ", end - start, " seconds\n")
    return end - start


def load_nodes_batch(nodes: pd.DataFrame, db):
    dict_results = {}
    dict_results["movie_genres"] = load_movie_genres_batch(
        parse_movie_generes(nodes), db
    )
    dict_results["colors"] = load_colors_batch(
        nodes["favourite_color"].dropna().unique().tolist(), db
    )
    dict_results["movies"], movie = load_movies_batch(
        nodes["favourite_movie"].dropna().unique().tolist(), db
    )
    dict_results["universities"], uni = load_universities_batch(
        nodes["university"].dropna().unique().tolist(), db
    )
    dict_results["countries"] = load_countries_batch(
        nodes.groupby(["country", "continent", "country_code"])
        .size()
        .reset_index()
        .drop_duplicates(),
        db,
    )
    dict_results["cities"], cities = load_cities_batch(parse_cities(nodes), db)
    dict_results["user"] = load_users_batch(nodes, db, movie, uni, cities)

    return dict_results


def user_movie_edge(user, user_id, db):
    if pd.isnull(user["favourite_movie"]):
        return {}
    query = "FOR movie IN Movie FILTER movie.title == @movie_title RETURN movie._id"
    movie_id = db.AQLQuery(
        query, bindVars={"movie_title": user["favourite_movie"]}, rawResults=True
    )
    if movie_id:
        return {"_from": user_id, "_to": movie_id[0]}
    return {}


def user_color_edge(user, user_id, db):
    if pd.isnull(user["favourite_color"]):
        return {}
    query = "FOR color IN Color FILTER color.name == @color_name RETURN color._id"
    color_id = db.AQLQuery(
        query, bindVars={"color_name": user["favourite_color"]}, rawResults=True
    )
    if color_id:
        return {"_from": user_id, "_to": color_id[0]}
    return {}


def user_university_edge(user, user_id, db):
    if pd.isnull(user["university"]):
        return {}
    query = "FOR university IN University FILTER university.name == @university_name RETURN university._id"
    university_id = db.AQLQuery(
        query, bindVars={"university_name": user["university"]}, rawResults=True
    )
    if university_id:
        return {"_from": user_id, "_to": university_id[0]}
    return {}


def user_city_edge(user, user_id, db):
    query = "FOR city IN City FILTER city.name == @city_name RETURN city._id"
    city_id = db.AQLQuery(query, bindVars={"city_name": user["city"]}, rawResults=True)
    if city_id:
        return {"_from": user_id, "_to": city_id[0]}
    return {}


def user_movie_genres_edge(user, user_id, db):
    genres = user["movie_genres"].split(",")

    genres = list(
        map(
            lambda x: x.replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace(" ", ""),
            genres,
        )
    )

    query = (
        "FOR genre IN MovieCategory FILTER genre.name == @genre_name RETURN genre._id"
    )

    edges = []

    for genre in genres:
        genre_id = db.AQLQuery(query, bindVars={"genre_name": genre}, rawResults=True)
        if genre_id:
            edges.append({"_from": user_id, "_to": genre_id[0]})


def load_country_city_edges_batches(db, cc_df):
    countries_query = "FOR country IN Country RETURN country"
    cities_query = "FOR city IN City RETURN city"

    countries = db.AQLQuery(countries_query, rawResults=True)
    cities = db.AQLQuery(cities_query, rawResults=True)
    docs = []

    for country in countries:
        list_of_cities = cc_df[cc_df["country"] == country["name"]]["city"].tolist()
        for city in cities:
            if city["name"] in list_of_cities:
                docs.append({"_from": country["_id"], "_to": city["_id"]})

    batches = [docs[i : i + batch_size] for i in range(0, len(docs), batch_size)]

    print("Loading country-city edges...\nSize: ", len(docs), "\n")
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["LocatedIn"]) for batch in batches
        ]
        for f in features:
            f.result()
    end = time.time()
    print("Country-city edges loaded in ", end - start, " seconds\n")
    return end - start


def load_user_edges_batch(edges: pd.DataFrame, db):
    pref = "User/"
    print("Loading user edges...\n" + "Size: ", len(edges), "\n")
    edges_list = list(zip(edges.src, edges.dest))

    docs = []
    for edge in edges_list:
        docs.append({"_from": pref + str(edge[0]), "_to": pref + str(edge[1])})

    batches = [docs[i : i + batch_size] for i in range(0, len(docs), batch_size)]

    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["Likes"]) for batch in batches
        ]
        for f in features:
            f.result()
    end = time.time()
    print("User edges loaded in ", end - start, " seconds\n")
    return end - start


def load_matches_batch(matches: pd.DataFrame, db):
    pref = "User/"
    print("Loading matches...\n" + "Size: ", len(matches), "\n")
    edges_list = list(zip(matches.src, matches.dest))

    docs = []
    for edge in edges_list:
        docs.append({"_from": pref + str(edge[0]), "_to": pref + str(edge[1])})

    batches = [docs[i : i + batch_size] for i in range(0, len(docs), batch_size)]

    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        features = [
            executor.submit(insert_batch, batch, db["Matches"]) for batch in batches
        ]
        for f in features:
            f.result()

    end = time.time()
    print("Matches loaded in ", end - start, " seconds\n")
    return end - start
