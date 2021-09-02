import pandas as pd
from pymongo import MongoClient
import time
from decimal import Decimal

# Init Mongo DB
MONGO_DETAILS = "mongodb://localhost:27017"

mongo_client = MongoClient(MONGO_DETAILS)

# Database Name
db = mongo_client.cryptocurrency_database
BTC_collection = db.BTC_collection

# Collection Name - ML
collection_cursor = BTC_collection.find()
df = list(collection_cursor)

# print(df)

def market_trend():
    time.sleep(10)

def buyer_strategy(order_book, open_orders, spreads):
    pass