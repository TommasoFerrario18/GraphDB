from pyArango.connection import *


## Letture
def get_user_data(user_id: str, db):
    query = "WITH User FOR u IN User FILTER u._id == @user RETURN u"
    return db.AQLQuery(query, bindVars={"user": "User/" + user_id})


def get_users_which_like_user(user_id: str, db):
    query = "WITH User FOR node, edge IN 1..1 INBOUND @user Likes RETURN node"
    return db.AQLQuery(query, bindVars={"user": "User/" + user_id})


def find_user_which_like_same_movie_category(user_id: str, db):
    query = """
    WITH User, MovieCategory
    FOR v, e IN 1..1 OUTBOUND @user IntMovieCategory 
        FOR v1, e1 IN 1..1 INBOUND v IntMovieCategory
            FILTER v1 != v
        RETURN v1
    """
    return db.AQLQuery(query, bindVars={"user": "User/" + user_id})


def get_all_users_which_live_in_same_city(user_id: str, db):
    query = """
    WITH User, City
    FOR v, e IN 1..1 OUTBOUND @user LivesIn 
        FOR v1, e1 IN 1..1 INBOUND v LivesIn
            FILTER v1 != v
        RETURN v1
    """
    return db.AQLQuery(query, bindVars={"user": "User/" + user_id})


def get_users_which_have_same_movie_and_studied_same_university(user_id: str, db):
    query = """
        WITH User, MovieCategory, University
        FOR v, e IN 1..1 OUTBOUND @user IntMovieCategory
            FOR v1, e1 IN 1..1 INBOUND v IntMovieCategory
                FILTER v1 != v
                FOR v2, e2 IN 1..1 OUTBOUND @user StudiesAt
                    FOR v3, e3 IN 1..1 INBOUND v2 StudiesAt
                        FILTER v3 != v2
                FILTER v3 == v1
        RETURN v3
    """
    return db.AQLQuery(query, bindVars={"user": "User/" + user_id})


def get_likes_of_user_match(user_id: str, db):
    query = """
    WITH User
    FOR v, e IN 1..1 ANY @user Matches
        FOR v1, e1 IN 1..1 OUTBOUND v Likes
    RETURN v1
    """
    return db.AQLQuery(query, bindVars={"user": "User/" + user_id})


def get_all_user_of_a_country(country_code: str, db):
    query = """
        WITH Country, City, User
        FOR city, edge IN 1..1 ANY  @country LocatedIn 
            FOR user, edge1 IN 1..1 ANY city LivesIn
        RETURN {"User": user._id, "City": city.name}
    """
    return db.AQLQuery(query, bindVars={"country": "Country/" + country_code})


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
    return db.AQLQuery(query)


## Cancellazione
def delete_user_py(user_id: str, db, graph):
    """Delete a user from the database using python code. This function deletes
    also the edges related to the user."""
    query = "WITH User FOR u IN User FILTER u._id == @user RETURN u"
    user = db.AQLQuery(query, bindVars={"user": user_id})
    if not user:
        print("User not found")
        return False
    print(user)
    return graph.deleteVertex(user[0])


def delete_user_AQL(user_id: str, db):
    """Delete a user from the database using AQL query."""
    query = "WITH User FOR u IN User FILTER u._id == @user REMOVE u IN User"
    return db.AQLQuery(query, bindVars={"user": user_id})


def delete_user_color_edge(user_id: str, db):
    query = """
        WITH IntColor
        FOR edge IN IntColor
            FILTER edge._from == @user
            REMOVE {_key: edge._key} IN IntColor
    """
    return db.AQLQuery(query, bindVars={"user": user_id})


## Modifica
def update_city(city_key: str, lat: float, lon: float, db):
    query = "UPDATE {_key: @city } WITH { lat:@lat, long: @long} IN City"
    return db.AQLQuery(query, bindVars={"city": city_key, "lat": lat, "long": lon})


def update_user_city_edge(user_key: str, city_key: str, db):
    query = """
        WITH LivesIn
        FOR edge in LivesIn 
            FILTER edge._from == @user 
            UPDATE {_key: edge._key} WITH {_to: @city} IN LivesIn
            """
    return db.AQLQuery(query, bindVars={"user": user_key, "city": city_key})

def replace_all_user_field(user_key: str, new_user: dict, db):
    query = """
        WITH User
        REPLACE {_key: @user} WITH @doc IN User
    """
    return db.AQLQuery(query, bindVars={"user": user_key, "doc": new_user})