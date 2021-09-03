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
            self.mongo_collection.insert_one(msg)

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
        # read json response
        raw_data = json.loads(res.content)
    
        for i in range(len(raw_data)):
            new_data = {
                "_id": raw_data[i][0],
                "cryptocurrency":crypto,
                "timestamp":raw_data[i][0],
                "low":raw_data[i][1],
                "high":raw_data[i][2],
                "open":raw_data[i][3],
                "close":raw_data[i][4],
                "volume":raw_data[i][5]
            }

            # MongoDB Dump
            BTC_collection.insert_one(new_data)

            # JSON Dump
            f.write(json.dumps(new_data))
            f.write('\n')
            # print(json.dumps(new_data))

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
        print('gaierror - connecting to Coinbase issue')
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
    # Fetch historical data
    start_date =  datetime.strptime("2017-01-01", "%Y-%m-%d")

    f = open("data/historical.json", "a")
    while(start_date.date() <= datetime.today().date()):
        getHistorical("ETH", start_date.date(),(start_date + timedelta(days=300)).date(),86400),
        start_date = (start_date+timedelta(days=300)) 
    f.close()

    # Fetch live data
    #getLive()

    order_book = Tree()

    # Collection Name - ML
    collection_cursor = BTC_collection.find()
    df = list(collection_cursor)
    print(df)
