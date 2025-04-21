from pymongo import MongoClient
from urllib.parse import quote_plus

username = "almohsinkhan"
password = quote_plus("Mohsin@2004")
uri = f"mongodb://{username}:{password}@cluster0.mongodb.net"

client = MongoClient(uri,  ssl=False)
print(client.list_database_names())
