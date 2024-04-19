from pyArango.collection import Edges, Field


class Likes(Edges):  # User - User
    _fields = {}


class Matches(Edges):  # User - User
    _fields = {}


class Interest(Edges):  # User - Movie & User - MovieCategory & User - Color
    _fields = {}


class Category(Edges):  # Movie - MovieCategory
    _fields = {}


class LivesIn(Edges):  # City - User
    _fields = {}


class StudiesAt(Edges):  # University - User
    _fields = {}


class LocatedIn(Edges):  # City - Country
    _fields = {}
