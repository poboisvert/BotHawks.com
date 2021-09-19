"""collectdata.py
Opens a subscription to real-time market and historical data via Coinbase PRO API
"""
import asyncio

import cbpro, sys
import logging
from cbpro.websocket_client import WebsocketClient
from socket import gaierror
from datetime import datetime, timedelta
import numpy
from pprint import pformat

import logging
import datetime as dt
import time, requests
import json
import argparse
from dateutil.tz import tzlocal
import pytz

from strategy.book import Book
from trading.openorders import OpenOrders

logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')

ARGS = argparse.ArgumentParser(description='Bot Recommendation')
ARGS.add_argument('--c', action='store_true', dest='command_line', default=False, help='Command line output')
ARGS.add_argument('--t', action='store_true', dest='trading', default=False, help='Trade')
args = ARGS.parse_args()

order_book = Book()
open_orders = OpenOrders()

class myWebsocketClient(WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["ETH-USD"]
        self.message_count = 0
        self.should_print = False
        self.channels = ["ticker"]
        self.msg = ''
        print("Lets count the messages!")

    def on_message(self, msg):
        self.message_count += 1
        self.msg = msg

    def on_close(self):
        print("-- Goodbye! --")

def getLive():
    """
    Description: load the fact table and the dim tables
    Arguments:
        cur: the cursor object. 
        conn: the conection to the postgresSQL.
    Returns:
        None
    """
    try:
        coinbase_websocket = myWebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="ETH-USD", should_print=False, channels=["ticker"])
        coinbase_websocket.start()
    except gaierror:
        print('socket.gaierror - No connection to Coinbase')
        return
    
    try:
        while True:
            print("\nMessageCount =", "%i \n" % coinbase_websocket.message_count)
        
            time.sleep(1)
            
            messages = []

            message = coinbase_websocket.msg
            # {'type': 'ticker', 'sequence': 20890370388, 'product_id': 'ETH-USD', 'price': '3390.6', 'open_24h': '3409.87', 'volume_24h': '123863.38933070', 'low_24h': '3377', 'high_24h': '3543', 'volume_30d': '5467679.65170842', 'best_bid': '3390.20', 'best_ask': '3390.60', 'side': 'buy', 'time': '2021-09-19T01:18:21.963162Z', 'trade_id': 157087756, 'last_size': '0.06209744'}
            messages += [message]

            if len(messages) > 20:
                break

            order_book.get_level3()
            [order_book.process_message(message) for message in messages if message['sequence'] > order_book.level3_sequence]

            messages = []
            if args.command_line:
                messages += [datetime.strptime(message['time'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.UTC)]
                #messages = [message for message in messages if (datetime.now(tzlocal()) - message).seconds < 60] # 1 MINUTE MSG TIMEOUT
                # [datetime.datetime(2021, 9, 19, 3, 30, 33, 96152, tzinfo=<UTC>)]
                print(messages)


                if len(messages) > 2:
                    diff = numpy.diff(messages)
                    print(diff)
                    diff = [float(sec.microseconds) for sec in diff]
                    order_book.average_rate = numpy.mean(diff)
                    order_book.fastest_rate = min(diff)
                    order_book.slowest_rate = max(diff)

                
            if not order_book.process_message(message):
                print(pformat(message))
                return False

    except KeyboardInterrupt:
        coinbase_websocket.close()


    if coinbase_websocket.error:
        sys.exit(1)
    else:
        sys.exit(0)

def monitor():
    time.sleep(5)
    while True:
        time.sleep(0.001)
        print('Last message: {0:.6f} secs, '
              'Min ask: {1:.2f}, Max bid: {2:.2f}, Spread: {3:.2f}, '
              'Your ask: {4:.2f}, Your bid: {5:.2f}, Your spread: {6:.2f} '
              'Avg: {7:.10f} Min: {8:.10f} Max: {9:.10f}'.format(
            ((datetime.now(tzlocal()) - order_book.last_time).microseconds * 1e-6),
            order_book.asks.price_tree.min_key(), order_book.bids.price_tree.max_key(),
            order_book.asks.price_tree.min_key() - order_book.bids.price_tree.max_key(),
            open_orders.decimal_open_ask_price, open_orders.decimal_open_bid_price,
            open_orders.decimal_open_ask_price - open_orders.decimal_open_bid_price,
            order_book.average_rate*1e-6, order_book.fastest_rate*1e-6, order_book.slowest_rate*1e-6), end='\r')

if __name__ == '__main__':
    if args.command_line:
        stream_handler = logging.StreamHandler()
    if args.command_line:
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, monitor)

    getLive()