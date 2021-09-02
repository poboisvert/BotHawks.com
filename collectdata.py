#This is the Python file to extract the songs from Spotify, transform the data and then load it into PostgreSQL.
#It is placed into a function for my Airflow DAG to call
import cbpro, time, sys
from pymongo import MongoClient
import logging
from cbpro.websocket_client import WebsocketClient

import logging
from pprint import pformat
from datetime import datetime

logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')

# specify the database and collection
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client.cryptocurrency_database
BTC_collection = db.BTC_collection


class myWebsocketClient(WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["ETH-USD"]
        self.message_count = 0
        self.mongo_collection = BTC_collection
        self.should_print = False
        self.channels = ["ticker"]
        print("Lets count the messages!")

    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print ("Message type:", msg["type"],
                   "\t@ {:.3f}".format(float(msg["price"])))

        if self.mongo_collection:  # dump JSON to given mongo collection
            self.mongo_collection.insert_one(msg)

    def on_close(self):
        print("-- Goodbye! --")

def collectData():
    # cbpro - INIT
    wsClient = myWebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="ETH-USD", mongo_collection=BTC_collection, should_print=False, channels=["ticker"])
    wsClient.start()

    # Logging Req - INIT
    #while (wsClient.message_count < 6):
    try:
        while True:
            print("\nMessageCount =", "%i \n" % wsClient.message_count)
            time.sleep(1)
    except KeyboardInterrupt:
        wsClient.close()
    #print(wsClient.mongo_collection)
    #wsClient.close()
    
    if wsClient.error:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    historical_datetime = datetime(year=2016, month=1, day=1,
                                   hour=0, minute=0, second=0)

    collectData()