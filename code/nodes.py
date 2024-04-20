from pyArango.collection import Collection, Field


class User(Collection):
    _fields = {
        "id": Field(),
        "first_name": Field(),
        "last_name": Field(),
        "email": Field(),
        "phone": Field(),
        "birth_date": Field(),
        "gender": Field(),
    }


class Movie(Collection):
    _fields = {"title": Field()}


class MovieCategory(Collection):
    _fields = {"name": Field()}


class City(Collection):
    _fields = {"name": Field(), "latitude": Field(), "longitude": Field()}


class Country(Collection):
    _fields = {"name": Field(), "code": Field(), "continent": Field()}


class University(Collection):
    _fields = {"name": Field()}


class Color(Collection):
    _fields = {"name": Field()}
