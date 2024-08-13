from arango import ArangoClient


## Letture
def get_user_data(user_id: str, db):
    query = "WITH User FOR u IN User FILTER u._id == @user RETURN u"
    return db.aql.execute(query, bind_vars={"user": user_id}, cache=False)


def get_users_which_like_user(user_id: str, db):
    query = "WITH User FOR user, edge IN 1..1 INBOUND @user Likes RETURN user"
    return db.aql.execute(query, bind_vars={"user": user_id}, cache=False)


def find_user_which_like_same_movie_category(user_id: str, db):
    query = """
    WITH User, MovieCategory
    FOR category, e IN 1..1 OUTBOUND @user IntMovieCategory
        FOR user, edge IN 1..1 INBOUND category IntMovieCategory
            FILTER user != @user
    RETURN category
    """
    return db.aql.execute(query, bind_vars={"user": user_id}, cache=False)


def get_all_users_which_live_in_same_city(user_id: str, db):
    query = """
    WITH User, City
    FOR city, e IN 1..1 OUTBOUND @user LivesIn 
        FOR user, edge IN 1..1 INBOUND city LivesIn
            FILTER user != @user
    RETURN user
    """
    return db.aql.execute(query, bind_vars={"user": user_id}, cache=False)


def get_users_which_have_same_movie_and_studied_same_university(user_id: str, db):
    query = """
    WITH User, MovieCategory, University
    FOR category, e IN 1..1 OUTBOUND @user IntMovieCategory
        FOR user1, e1 IN 1..1 INBOUND category IntMovieCategory
                FILTER user1 != @user
        FOR colleague, e2 IN 1..1 OUTBOUND @user StudiesAt
            FOR user2, e3 IN 1..1 INBOUND colleague StudiesAt
                FILTER user2 != @user
            FILTER user1 == user2
    RETURN user1
    """
    return db.aql.execute(query, bind_vars={"user": user_id}, cache=False)


def get_likes_of_user_match(user_id: str, db):
    query = """
    WITH User
    FOR v, e IN 1..1 ANY @user Matches
        FOR v1, e1 IN 1..1 OUTBOUND v Likes
    RETURN v1
    """
    return db.aql.execute(query, bind_vars={"user": "User/" + user_id}, cache=False)


def get_all_user_of_a_country(country_code: str, db):
    query = """
        WITH Country, City, User
        FOR city, edge IN 1..1 ANY  @country LocatedIn 
            FOR user, edge1 IN 1..1 ANY city LivesIn
        RETURN {"User": user._id, "City": city.name}
    """
    return db.aql.execute(
        query, bind_vars={"country": "Country/" + country_code}, cache=False
    )


def get_number_of_users_in_city(db):
    query = """
        WITH City, User
        FOR city IN City
            LET usersCount = LENGTH(
                FOR v, e, p IN 1..1 INBOUND city LivesIn
                RETURN v
            )
        RETURN { city: city.name, numberOfUsers: usersCount }
    """
    return db.aql.execute(query, cache=False)


def get_city(city: str, db):
    query = "WITH City FOR city IN City FILTER city._key == @city RETURN city"
    return db.aql.execute(query, bind_vars={"city": city}, cache=False)


def get_all_user(db):
    query = "FOR u IN User RETURN u"
    return db.aql.execute(query, cache=False)


def get_movie_like_and_match(user_id: str, db):
    query = """
    WITH User, Movie
    FOR match, e IN 1..1 OUTBOUND @user Likes
        FOR user, edge_like IN 1..1 OUTBOUND match._id Likes
            FOR movie, edge_movie IN 1..1 ANY user._id IntMovie
    RETURN DISTINCT movie
    """
    return db.aql.execute(query, bind_vars={"user": user_id}, cache=False)


## Cancellazione
def delete_user_py(user_id: str, db, graph):
    """Delete a user from the database using python code. This function deletes
    also the edges related to the user."""
    query = "WITH User FOR u IN User FILTER u._id == @user RETURN u"
    user = db.aql.execute(query, bind_vars={"user": user_id})
    users = [doc for doc in user]
    if not users:
        print("User not found")
        return False
    print(users)
    return graph.delete_vertex(users[0])


def delete_user_AQL(user_id: str, db):
    """Delete a user from the database using AQL query."""
    query = "WITH User FOR u IN User FILTER u._id == @user REMOVE u IN User"
    return db.aql.execute(query, bind_vars={"user": user_id})


def delete_user_color_edge(user_id: str, db):
    query = """
        WITH IntColor
        FOR edge IN IntColor
            FILTER edge._from == @user
            REMOVE {_key: edge._key} IN IntColor
    """
    return db.aql.execute(query, bind_vars={"user": user_id})


## Modifica
def update_city(city_key: str, lat: float, lon: float, db):
    query = "UPDATE {_key: @city } WITH { lat:@lat, long: @long} IN City"
    return db.aql.execute(query, bind_vars={"city": city_key, "lat": lat, "long": lon})


def update_user_city_edge(user_key: str, city_key: str, db):
    query = """
        WITH LivesIn
        FOR edge in LivesIn 
            FILTER edge._from == @user 
            UPDATE {_key: edge._key} WITH {_to: @city} IN LivesIn
            """
    return db.aql.execute(query, bind_vars={"user": user_key, "city": city_key})


def replace_all_user_field(user_key: str, new_user: dict, db):
    query = """
        WITH User
        REPLACE {_key: @user} WITH @doc IN User
    """
    return db.aql.execute(query, bind_vars={"user": user_key, "doc": new_user})


def simulating_node_failure(
    graph, db, user_id: str, country_code: str, city_key: str, lat: float, lon: float
):
    print("Simulating node failure")
    print("Reading data")
    cursor = get_all_user_of_a_country(country_code=country_code, db=db)
    print("Data read: ", len([doc for doc in cursor]))
    print("Deleting user")
    user = get_user_data(user_id, db)
    list_user = [doc for doc in user]
    print("User read", list_user)
    delete_user_py(user_id, db, graph)
    delete_vertex = [doc for doc in get_user_data(user_id, db)]
    print("User deleted", len(delete_vertex))
    print("Inserting user")

    user_node = list_user[0]
    del user_node["_id"]
    del user_node["_rev"]
    del user_node["_key"]

    graph.insert_vertex("User", list_user[0])
    print("User inserted")
    print("Updating user")
    update_city(city_key, lat, lon, db)
    l = [doc for doc in get_city(city_key, db)]
    print("City updated", l)


def update_all_city(db):
    query = """FOR city IN City 
    UPDATE {_key: city._key} WITH { lat:@lat, long: @long} IN City"""
    return db.aql.execute(query, bind_vars={"lat": 0, "long": 0})


def update_all_like(db):
    query = """FOR edge IN Likes 
    UPDATE {_key: edge._key} WITH {vote:@vote} IN Likes"""
    return db.aql.execute(query, bind_vars={"vote": 9})
