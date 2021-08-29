#This is the Python file to extract the songs from Spotify, transform the data and then load it into PostgreSQL.
#It is placed into a function for my Airflow DAG to call
import cbpro, time
from pymongo import MongoClient
import logging

logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')

# specify the database and collection
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client.cryptocurrency_database
BTC_collection = db.BTC_collection


class myWebsocketClient(cbpro.WebsocketClient):
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
    from pymongo import MongoClient
    import cbpro
    mongo_client = MongoClient('mongodb://localhost:27017/')

    # Mongo DB - INIT
    db = mongo_client.cryptocurrency_database
    BTC_collection = db.BTC_collection

    # cbpro - INIT
    wsClient = myWebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="ETH-USD", mongo_collection=BTC_collection, should_print=False, channels=["ticker"])
    wsClient.start()

    # Logging Req - INIT
    while (wsClient.message_count < 52):
        print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
        time.sleep(1)

    #print(wsClient.mongo_collection)
    wsClient.close()

if __name__ == '__main__':
    collectData()