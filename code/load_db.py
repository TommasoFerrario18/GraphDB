import pandas as pd
from pyArango.connection import *

def create_db():
    conn = Connection()

    try:
        conn.createDatabase(name="SoulSync")
    except CreationError:
        print("Couldn't create database, it probably already exists")
        pass

    db = conn["SoulSync"]

    try:
        db.createGraph("SoulSyncGraph")
    except CreationError:
        print("Couldn't create graph, it probably already exist")
        pass

    my_graph = db.graphs["SoulSyncGraph"]
    
    return db, my_graph

def get_movie_genres(nodes):

    rows = nodes["movie_genres"].apply(lambda x: x.split(","))

    rows = rows.apply(
        lambda x: [
            i.replace("[", "").replace("]", "").replace("'", "").replace(" ", "") for i in x
        ]
    )

    flat_list = [x for xs in rows.to_list() for x in xs]

    movie_genres = pd.Series(flat_list).unique().tolist()

    return movie_genres

# Load movie, movie category, color, university, city and country nodes
def load_basic_nodes(nodes, my_graph):

    try:

        movie_genres = get_movie_genres(nodes)

        for genre in movie_genres:
            my_graph.createVertex("MovieCategory", {"_key": genre, "name": genre})

        colors = nodes["favourite_color"].dropna().unique().tolist()
        for color in colors:
            my_graph.createVertex("Color", {"_key": color, "name": color})

        movies = nodes["favourite_movie"].dropna().unique().tolist()
        for movie in movies:
            my_graph.createVertex("Movie", {"title": movie})

        universities = nodes["university"].dropna().unique().tolist()
        for university in universities:
            my_graph.createVertex("University", {"name": university})


        country_combinations = nodes.groupby(['country', 'continent', "country_code"]).size().reset_index().drop_duplicates()

        for row in country_combinations.iterrows():
            row = row[1]
            name = ["country"]
            code = row["country_code"]
            continent = row["continent"]
            my_graph.createVertex("Country", {"name": name, "code": code, "continent": continent})

        city_combinations = nodes.groupby(['city', 'lat', "long"]).size().reset_index().drop_duplicates()

        for row in city_combinations.iterrows():
            row = row[1]
            name = row["city"]
            lat = row["lat"]
            long = row["long"]
            my_graph.createVertex("City", {"name": name, "latitude": lat, "longitude": long})

    except:
        print("Couldn't load basic nodes")

def load_users(nodes, my_graph):
    for row in nodes.iterrows():
        #print(row)
        row=row[1]
        my_graph.createVertex("User", {
            "_key": str(row["id"]),
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "phone": row["phone"],
            "birth_date": row["birthDate"],
            "gender": row["gender"]
            })