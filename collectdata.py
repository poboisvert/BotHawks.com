#This is the Python file to extract the songs from Spotify, transform the data and then load it into PostgreSQL.
#It is placed into a function for my Airflow DAG to call
import cbpro, time

from pymongo import MongoClient
mongo_client = MongoClient('mongodb://localhost:27017/')

import logging

# specify the database and collection
db = mongo_client.cryptocurrency_database
BTC_collection = db.BTC_collection

logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')

def spotify_etl_func():
    # Get the order book at a specific level.
    # Parameters are optional
    # instantiate a WebsocketClient instance, with a Mongo collection as a parameter
    wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="BTC-USD",
        mongo_collection=BTC_collection, should_print=False)
    wsClient.start()
    # Do other stuff...
    wsClient.close()


if __name__ == '__main__':
    spotify_etl_func()