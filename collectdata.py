#This is the Python file to extract the songs from Spotify, transform the data and then load it into PostgreSQL.
#It is placed into a function for my Airflow DAG to call
import cbpro, sys
from pymongo import MongoClient
import logging
from cbpro.websocket_client import WebsocketClient
from strategy.statistics import Tree
from socket import gaierror
from datetime import datetime, timedelta

import logging
import datetime as dt
import requests, time
import json, bson

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
            #self.mongo_collection.insert_one(msg)
            # print(msg)
            product_id = 0
            price = 0
            volume_24h = 0
            high_24h = 0
            low_24h = 0
            time = 0
            volume = 0

            for key, value in msg.items():
                if key=="product_id":
                    product_id = value
                else:
                    pass

                if key=="price":
                    price = value
                else:
                    pass

                if key=="volume_24h":
                    volume_24h = value
                else:
                    pass

                if key=="high_24h":
                    high_24h = value
                else:
                    pass

                if key=="low_24h":
                    low_24h = value
                else:
                    pass

                if key=="time":
                    time = value
                else:
                    pass

                if key=="last_size":
                    volume = value
                else:
                    pass

                new_data = {
                    "cryptocurrency":product_id,
                    "timestamp":time,
                    "low":low_24h,
                    "high":high_24h,
                    "open":price,
                    "close":high_24h,
                    "volume":volume_24h,
                }
                #print(new_data)
                self.mongo_collection.insert_one(new_data)
            return('Key Not Found')


    def on_close(self):
        print("-- Goodbye! --")

# real time data collector
def getHistorical(crypto,start_date,end_date,gran):

    t_0 = time.time()
    # call API
    URL = 'https://api.pro.coinbase.com/products/{0}-{1}/{2}?start={3}&end={4}&granularity={5}'.format(crypto, "USD", 'candles',start_date,end_date,gran)
    #print(uri)
    res = requests.get(URL)

    if (res.status_code==200):
        # Read json response
        raw_data = json.loads(res.content)
    
        for i in range(len(raw_data)):

            # Format
            new_data = {
                "cryptocurrency":crypto,
                "timestamp":raw_data[i][0],
                "low":raw_data[i][1],
                "high":raw_data[i][2],
                "open":raw_data[i][3],
                "close":raw_data[i][4],
                "volume":raw_data[i][5]
            }

            # Write JSON
            f.write(json.dumps(new_data))
            f.write('\n')
            #print(json.dumps(new_data))

            # MongoDB
            double_id = BTC_collection.find_one(raw_data[i][0])

            if double_id is None:
                BTC_collection.insert_one(new_data)

        # debug / print message
        print('API request at time {0}'.format(dt.datetime.utcnow()))
        
    else:
        print('Failed API request at time {0}'.format(dt.datetime.utcnow()))

def getLive():
    # cbpro - INIT
    try:
        wsClient = myWebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="ETH-USD", mongo_collection=BTC_collection, should_print=False, channels=["ticker"])
        wsClient.start()
    except gaierror:
        print('socket.gaierror - had a problem connecting to Coinbase feed')
        return

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
    start_date =  datetime.strptime("2019-01-01", "%Y-%m-%d")



    # { "_id" : ObjectId("613295033449e25402609069"), "cryptocurrency" : "ETH", "timestamp" : 1570665600, "low" : 187.29, "high" : 194.85, "open" : 193.26, "close" : 191.79, "volume" : 86674.1411952 }
    
    # Fetch live
    getLive()

    # { "_id" : ObjectId("613297483449e25473531591"), "type" : "ticker", "sequence" : NumberLong("20448265771"), "product_id" : "ETH-USD", "price" : "3933.53", "open_24h" : "3830.58", "volume_24h" : "272162.52500599", "low_24h" : "3710.59", "high_24h" : "4030.35", "volume_30d" : "6015365.39397879", "best_bid" : "3933.37", "best_ask" : "3933.53", "side" : "buy", "time" : "2021-09-03T21:44:40.982168Z", "trade_id" : 151717814, "last_size" : "0.74491454" }

    order_book = Tree()
    # Collection Name - ML
    collection_cursor = BTC_collection.find()
    df = list(collection_cursor)
    #print(df)
