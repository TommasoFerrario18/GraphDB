from pyArango.collection import Edges, Field


class Likes(Edges):  # User - User
    _fields = {}


class Matches(Edges):  # User - User
    _fields = {}


class IntMovie(Edges):  # User - Movie
    _fields = {}


class IntMovieCategory(Edges):  # User - MovieCategory
    _fields = {}


class IntColor(Edges):  # User - Color
    _fields = {}


# class Category(Edges):  # Movie - MovieCategory
#     _fields = {}


class LivesIn(Edges):  # City - User
    _fields = {}


class StudiesAt(Edges):  # University - User
    _fields = {}


class LocatedIn(Edges):  # City - Country
    _fields = {}

class CountryLocatedIn(Edges):  # Country - Continent
    _fields = {}
