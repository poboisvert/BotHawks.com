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

class myWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["BTC-USD"]
        self.message_count = 0
        self.mongo_collection = "BTC_collection"
        self.should_print = False
        print("Lets count the messages!")

    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print ("Message type:", msg["type"],
                   "\t@ {:.3f}".format(float(msg["price"])))
    def on_close(self):
        print("-- Goodbye! --")

def spotify_etl_func():
    from pymongo import MongoClient
    import cbpro
    mongo_client = MongoClient('mongodb://localhost:27017/')

    # specify the database and collection
    db = mongo_client.cryptocurrency_database
    BTC_collection = db.BTC_collection

    # instantiate a WebsocketClient instance, with a Mongo collection as a parameter
    wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="ETH-USD",
        mongo_collection=BTC_collection, should_print=False, channels=["ticker"])
    wsClient.start()

if __name__ == '__main__':
    spotify_etl_func()