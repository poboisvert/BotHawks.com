import pandas as pd
from pymongo import MongoClient
import time
from decimal import Decimal
import requests
from bintrees import FastRBTree

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
class Tree(object):
    def __init__(self):
        self.price_tree = FastRBTree()
        self.price_map = {}
        self.order_map = {}
        self.received_orders = {}

    def receive(self, order_id, size):
        self.received_orders[order_id] = size

    def create_price(self, price):
        new_list = []
        self.price_tree.insert(price, new_list)
        self.price_map[price] = new_list

    def remove_price(self, price):
        self.price_tree.remove(price)
        del self.price_map[price]

    def insert_order(self, order_id, size, price, initial=False):
        if not initial:
            del self.received_orders[order_id]
        if price not in self.price_map:
            self.create_price(price)
        order = {'order_id': order_id, 'size': size, 'price': price, 'price_map': self.price_map[price]}
        self.price_map[price].append(order)
        self.order_map[order_id] = order

    def match(self, maker_order_id, match_size):
        order = self.order_map[maker_order_id]
        original_size = order['size']
        new_size = original_size - match_size
        order['size'] = new_size

    def change(self, order_id, new_size):
        order = self.order_map[order_id]
        order['size'] = new_size

    def remove_order(self, order_id):
        if order_id in self.order_map:
            order = self.order_map[order_id]
            self.price_map[order['price']] = [o for o in self.price_map[order['price']] if o['order_id'] != order_id]
            if not self.price_map[order['price']]:
                self.remove_price(order['price'])
            del self.order_map[order_id]
        else:
            del self.received_orders[order_id]

    def sma_all():
        moving_averages = []
        window_size = 3

        while i < len(numbers) - window_size + 1:
            this_window = numbers[i : i + window_size]

            window_average = sum(this_window) / window_size
            moving_averages.append(window_average)
            i += 1


    def buyer_strategy(order_book, open_orders, spreads):
        pass

#filter_id = Tree('MVV')
#print(filter_id.name)