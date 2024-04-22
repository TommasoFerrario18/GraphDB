import time
import pandas as pd
from utils import *
from pyArango.connection import *


# Create a database and all the collections and graphs needed
def create_db():
    # Create a connection to the database
    conn = Connection()

    # Create the database
    try:
        conn.createDatabase(name="SoulSync")
    except CreationError:
        print("Couldn't create database, it probably already exists")
        pass

    # Connect to the database
    db = conn["SoulSync"]

    # Create the graph
    try:
        db.createGraph("SoulSyncGraph")
    except CreationError:
        print("Couldn't create graph, it probably already exist")
        pass

    return db, db.graphs["SoulSyncGraph"]


# Load Data
def load_movies(movies: list, graph):
    print("Loading movies...\nSize: ", len(movies), "\n")
    start = time.time()
    for movie in movies:
        graph.createVertex("Movie", {"title": movie})
    end = time.time()
    print("Movies loaded in ", end - start, " seconds\n")


def load_movie_genres(movie_genres: list, graph):
    print("Loading movie genres...\nSize: ", len(movie_genres), "\n")
    start = time.time()
    for genre in movie_genres:
        if genre == "nan" or genre == "(nogenreslisted)":
            continue
        graph.createVertex("MovieCategory", {"_key": genre, "name": genre})
    end = time.time()
    print("Movie genres loaded in ", end - start, " seconds\n")


def load_colors(colors: list, graph):
    print("Loading colors...\nSize: ", len(colors), "\n")
    start = time.time()
    for color in colors:
        graph.createVertex("Color", {"_key": color, "name": color})
    end = time.time()
    print("Colors loaded in ", end - start, " seconds\n")


def load_universities(universities: list, graph):
    print("Loading universities...\nSize: ", len(universities), "\n")
    start = time.time()
    for university in universities:
        graph.createVertex("University", {"name": university})
    end = time.time()
    print("Universities loaded in ", end - start, " seconds\n")


def load_cities(cities: dict, graph):
    print("Loading cities...\nSize: ", len(cities), "\n")
    start = time.time()
    for city in cities:
        city_info = cities[city]
        graph.createVertex(
            "City",
            {"name": city},
        )
    end = time.time()
    print("Cities loaded in ", end - start, " seconds\n")


def load_countries(countries: pd.DataFrame, graph):
    print("Loading countries...\nSize: ", len(countries), "\n")
    start = time.time()
    for row in countries.iterrows():
        row = row[1]
        name = row["country"]
        code = row["country_code"]
        continent = row["continent"]
        graph.createVertex(
            "Country",
            {"_key": code, "name": name, "code": code, "continent": continent},
        )
    end = time.time()
    print("Countries loaded in ", end - start, " seconds\n")


def load_users(nodes: pd.DataFrame, graph, db):
    print("Loading users...\nSize: ", len(nodes), "\n")
    start = time.time()
    for row in nodes.iterrows():
        id = row[0]
        row = row[1]
        user = graph.createVertex(
            "User",
            {
                "_key": str(id),
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "phone": row["phone"],
                "birth_date": row["birthDate"],
                "gender": row["gender"],
                "latitude": row["lat"],
                "longitude": row["long"]
            },
        )
        load_movie_genre_edges(row, user._id, graph, db)
        load_movie_edges(row, user._id, graph, db)
        load_color_edges(row, user._id, graph, db)
        load_university_edges(row, user._id, graph, db)
        load_city_edges(row, user._id, graph, db)

    end = time.time()
    print("Users loaded in ", end - start, " seconds\n")


def load_basic_nodes(nodes: pd.DataFrame, my_graph, db):
    load_movie_genres(parse_movie_generes(nodes), my_graph)
    load_colors(nodes["favourite_color"].dropna().unique().tolist(), my_graph)
    load_movies(nodes["favourite_movie"].dropna().unique().tolist(), my_graph)
    load_universities(nodes["university"].dropna().unique().tolist(), my_graph)
    load_countries(
        nodes.groupby(["country", "continent", "country_code"])
        .size()
        .reset_index()
        .drop_duplicates(),
        my_graph,
    )
    load_cities(parse_cities(nodes), my_graph)
    load_users(nodes, my_graph, db)


def load_country_city_edges(db, graph, cc_df):
    countries_query = "FOR country IN Country RETURN country"
    cities_query = "FOR city IN City RETURN city"

    countries = db.AQLQuery(countries_query, rawResults=True)
    cities = db.AQLQuery(cities_query, rawResults=True)

    print("Loading country-city edges...\n")
    start = time.time()
    for country in countries:
        list_of_cities = cc_df[cc_df["country"] == country["name"]]["city"].tolist()
        for city in cities:
            if city["name"] in list_of_cities:
                graph.createEdge("LocatedIn", country["_id"], city["_id"], {})

    end = time.time()
    print("Country-city edges loaded in ", end - start, " seconds\n")


def load_user_edges(edges: pd.DataFrame, graph):
    pref = "User/"
    start = time.time()
    print("Loading user edges...\n" + "Size: ", len(edges), "\n")
    edges.apply(
        lambda row: graph.createEdge(
            "Likes", pref + str(row["src"]), pref + str(row["dest"]), {}
        ),
        axis=1,
    )
    end = time.time()
    print("User edges loaded in ", end - start, " seconds\n")


def load_movie_edges(user, user_id, graph, db):
    if pd.isnull(user["favourite_movie"]):
        return
    query = "FOR movie IN Movie FILTER movie.title == @movie_title RETURN movie._id"
    movie_id = db.AQLQuery(
        query, bindVars={"movie_title": user["favourite_movie"]}, rawResults=True
    )
    graph.createEdge("IntMovie", user_id, movie_id[0], {})


def load_color_edges(user, user_id, graph, db):
    if pd.isnull(user["favourite_color"]):
        return
    query = "FOR color IN Color FILTER color.name == @color_name RETURN color._id"
    color_id = db.AQLQuery(
        query, bindVars={"color_name": user["favourite_color"]}, rawResults=True
    )
    graph.createEdge("IntColor", user_id, color_id[0], {})


def load_university_edges(user, user_id, graph, db):
    if pd.isnull(user["university"]):
        return
    query = "FOR university IN University FILTER university.name == @university_name RETURN university._id"
    university_id = db.AQLQuery(
        query, bindVars={"university_name": user["university"]}, rawResults=True
    )
    graph.createEdge("StudiesAt", user_id, university_id[0], {})


def load_city_edges(user, user_id, graph, db):
    query = "FOR city IN City FILTER city.name == @city_name RETURN city._id"
    city_id = db.AQLQuery(query, bindVars={"city_name": user["city"]}, rawResults=True)
    graph.createEdge("LivesIn", user_id, city_id[0], {})


def load_movie_genre_edges(user, user_id, graph, db):
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

    for genre in genres:
        genre_id = db.AQLQuery(query, bindVars={"genre_name": genre}, rawResults=True)
        if genre_id:
            graph.createEdge("IntMovieCategory", user_id, genre_id[0], {})

def load_matches(matches: pd.DataFrame, graph):
    pref = "User/"
    start = time.time()
    print("Loading matches...\n" + "Size: ", len(matches), "\n")
    matches.apply(
        lambda row: graph.createEdge(
            "Matches", pref + str(row["src"]), pref + str(row["dest"]), {}
        ),
        axis=1,
    )
    end = time.time()
    print("Matches loaded in ", end - start, " seconds\n")