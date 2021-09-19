"""collectdata.py
Opens a subscription to real-time market and historical data via Coinbase PRO API
"""
import cbpro, sys
from pymongo import MongoClient
import logging
from cbpro.websocket_client import WebsocketClient
from socket import gaierror
from datetime import datetime, timedelta

import logging
import datetime as dt
import time, requests
import json
import argparse

logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')

parser = argparse.ArgumentParser(description='Punisher Dash Vizualizer')
parser.add_argument('-n', '--name', help='name of your experiment', default='default', type=str)


# specify the database and collection
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client.cryptocurrency_database
BTC_collection = db.BTC_collection

# real time data collector
def getHistorical(crypto,start_date,end_date,gran):
    """
    Description: load the fact table and the dim tables
    Arguments:
        cur: the cursor object. 
        conn: the conection to the postgresSQL.
    Returns:
        None
    """
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

if __name__ == '__main__':
    start_date =  datetime.strptime("2018-09-01", "%Y-%m-%d")

    # Logging Req
    f = open("data/historical.json", "a")
    while(start_date.date() <= datetime.today().date()):
        getHistorical("ETH", start_date.date(),(start_date + timedelta(days=300)).date(),86400),
        start_date = (start_date+timedelta(days=300)) 
    f.close()

    # Collection Name - ML
    collection_cursor = BTC_collection.find()
    df = list(collection_cursor)