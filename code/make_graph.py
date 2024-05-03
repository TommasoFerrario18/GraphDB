from pyArango.graph import Graph, EdgeDefinition
from nodes import *
from edges import *

class SoulSyncGraph(Graph):
    _edgeDefinitions = [
        EdgeDefinition("Likes", fromCollections=["User"], toCollections=["User"]),
        EdgeDefinition("Matches", fromCollections=["User"], toCollections=["User"]),
        EdgeDefinition("IntMovie", fromCollections=["User"], toCollections=["Movie"]),
        EdgeDefinition("IntColor", fromCollections=["User"], toCollections=["Color"]),
        EdgeDefinition("IntMovieCategory", fromCollections=["User"], toCollections=["MovieCategory"]),
        EdgeDefinition("LivesIn", fromCollections=["User"], toCollections=["City"]),
        EdgeDefinition("LocatedIn", fromCollections=["City"], toCollections=["Country"]),
        EdgeDefinition("StudiesAt", fromCollections=["User"], toCollections=["University"])
        ]
    #     EdgeDefinition("Category", fromCollections=["Movie"], toCollections=["MovieCategory"])
    #     ]
    _orphanedCollections = []
