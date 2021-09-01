import pandas as pd
from pymongo import MongoClient

# Init Mongo DB
MONGO_DETAILS = "mongodb://localhost:27017"

mongo_client = MongoClient(MONGO_DETAILS)

# Database Name
db = mongo_client.cryptocurrency_database
BTC_collection = db.BTC_collection

# Collection Name - ML
collection_cursor = BTC_collection.find()
df = pd.DataFrame(list(collection_cursor))

print(df)