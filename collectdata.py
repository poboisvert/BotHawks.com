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
            #self.mongo_collection.insert_one(msg) # RAW to MongoDB

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
                if key=="price":
                    price = value
                if key=="volume_24h":
                    volume_24h = value
                if key=="high_24h":
                    high_24h = value
                if key=="low_24h":
                    low_24h = value
                if key=="time":
                    time = value
                if key=="last_size":
                    volume = value

                new_data = {
                    "cryptocurrency":product_id,
                    "timestamp":time,
                    "low":low_24h,
                    "high":high_24h,
                    "open":price,
                    "close":high_24h,
                    "volume":volume_24h,
                }

                self.mongo_collection.insert_one(new_data)
            return('Key Not Found')


    def on_close(self):
        print("-- Goodbye! --")

# real time data collector
def getHistorical(crypto,start_date,end_date,gran):

    # call API
    URL = 'https://api.pro.coinbase.com/products/{0}-{1}/{2}?start={3}&end={4}&granularity={5}'.format(crypto, "USD", 'candles',start_date,end_date,gran)
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

            # MongoDB
            double_id = BTC_collection.find_one(raw_data[i][0])

            if double_id is None:
                BTC_collection.insert_one(new_data)

        # debug / print message
        print('SUCCESS API request at time {0}'.format(dt.datetime.utcnow()))
        
    else:
        print('FAILED API request at time {0}'.format(dt.datetime.utcnow()))

def getLive():
    # cbpro - INIT
    try:
        wsClient = myWebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="ETH-USD", mongo_collection=BTC_collection, should_print=False, channels=["ticker"])
        wsClient.start()
    except gaierror:
        print('socket.gaierror - No connection to Coinbase')
        return

    # Logging Req - INIT
    #while (wsClient.message_count < 6):
    try:
        while True:
            print("\nMessageCount =", "%i \n" % wsClient.message_count)
            time.sleep(1)
    except KeyboardInterrupt:
        wsClient.close()

    if wsClient.error:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    start_date =  datetime.strptime("2018-09-01", "%Y-%m-%d")

    # Logging Req
    f = open("data/historical.json", "a")
    while(start_date.date() <= datetime.today().date()):
        getHistorical("ETH", start_date.date(),(start_date + timedelta(days=300)).date(),86400),
        start_date = (start_date+timedelta(days=300)) 
    f.close()

    # Fetch live
    #getLive()

    order_book = Tree()
    # Collection Name - ML
    collection_cursor = BTC_collection.find()
    df = list(collection_cursor)
    #print(df)
