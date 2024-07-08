from insert import *
from utils import *
from analysis import *
from query import *
from database import *
import time

typeDB = 1  # 0 for centralized, 1 for distributed

client = ArangoClient(hosts=["http://localhost:8000", "http://localhost:8001"])

# Connect to "_system" database as root user.
db = client.db("SoulSync", username="", password="")

cluster_info = db.cluster.server_count()

# Stampare le informazioni del cluster
print(cluster_info)
