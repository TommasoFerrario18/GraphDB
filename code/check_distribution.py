from arango import ArangoClient

# Connettersi al client ArangoDB
client = ArangoClient(hosts=["http://localhost:8000", "http://localhost:8001"])


# Connettersi al database
db = client.db("SoulSync", username="", password="")

# Ottenere l'elenco delle collezioni
collections = db.collections()


# Funzione per ottenere informazioni sugli shard di una collezione
def get_shard_distribution(collection_name):
    col = db.collection(collection_name)
    shard_info = col.shards()
    return shard_info


# Iterare attraverso le collezioni e ottenere la distribuzione degli shard
for collection in collections:
    # if collection["_system"]:
    #     continue  # Salta le collezioni di sistema
    collection_name = collection["name"]
    shard_distribution = get_shard_distribution(collection_name)
    print(f"Shard distribution for collection '{collection_name}':")
    for shard_id, servers in shard_distribution.items():
        print(f"  Shard {shard_id} is stored on servers: {servers}")
