from pyArango.connection import *
from nodes import *
from edges import *
from pyArango.graph import Graph, EdgeDefinition
from make_graph import SoulSyncGraph
import pandas as pd
from load_db import *

db, my_graph = create_db()

users = pd.read_csv("./data/nodes.csv").drop(["Unnamed: 0"], axis=1)

load_basic_nodes(users, my_graph)
