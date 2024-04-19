from pyArango.connection import *
from nodes import *
from edges import *
from pyArango.graph import Graph, EdgeDefinition


conn = Connection()

db = conn.createDatabase("SoulSync")

