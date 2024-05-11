from pyArango.connection import *

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