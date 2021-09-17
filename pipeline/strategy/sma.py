import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np

from datetime import datetime, timedelta
import plotly.express as px
import argparse

import matplotlib.pyplot as plt

mongo_client = MongoClient('localhost', 27017)

db = mongo_client.cryptocurrency_database
BTC_collection = db.BTC_collection

collection_cursor = BTC_collection.find()

parser = argparse.ArgumentParser(description='Moving Average Charts')

class sma():
    def __init__(self, asset, quantity):
        self.asset = asset
        self.quantity = quantity

    def __init__(self, asset, quantity):
        super().__init__()
        self.asset = asset
        self.quantity = quantity

    def movingAVG():
        df = pd.DataFrame(collection_cursor)

        df['date'] = pd.to_datetime(df['timestamp'], unit = 's')
        df.set_index('date', inplace=True)
        df = df.sort_values(by='date', ascending=True).copy()

        fig = px.line(df, y="close", title='ETH Stock Price', labels = {'close':'ETH Close Price(in USD)'})
        fig.show()
        plt.savefig('books_read.png')

        window1 = 5
        window2 = 9

        sma1 = pd.DataFrame()
        sma1['close'] = df['close'].rolling(window = window1).mean()

        sma2 = pd.DataFrame()
        sma2['close'] = df['close'].rolling(window = window2).mean()

        data = pd.DataFrame()
        data['ETH'] = df['close']
        data['SMA'+str(window1)] = sma1['close']
        data['SMA'+str(window2)] = sma2['close']
        def dualMACrossover(data):
            sigPriceBuy = []
            sigPriceSell = []
            flag = -1 # Flag denoting when the 2 moving averages crossed each other
            for i in range(len(data)):
                if data['SMA'+str(window1)][i] > data['SMA'+str(window2)][i]:
                    if flag != 1:
                        sigPriceBuy.append(data['ETH'][i])
                        sigPriceSell.append(np.nan)
                        flag = 1
                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)
                elif data['SMA'+str(window1)][i] < data['SMA'+str(window2)][i]:
                    if flag!=0:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(data['ETH'][i])
                        flag=0
                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
            return (sigPriceBuy,sigPriceSell)

        buy_sell = dualMACrossover(data)
        data['BuySignalPrice'] = buy_sell[0]
        data['SellSignalPrice'] = buy_sell[1]

        print(buy_sell)

        # print(("To visualize, run: `python -m punisher.charts.dash_charts.dash_record --name {:s}`\n").format(experiment_name))

        import plotly.graph_objects as go

        fig = px.line(data, y="ETH", title='Strategy Visualization', labels = {'index':'Date'})
        fig.add_scatter(x=data.index,y=data['SMA'+str(window1)], mode='lines',name='SMA'+str(window1))
        fig.add_scatter(x=data.index,y=data['SMA'+str(window2)], mode='lines',name='SMA'+str(window2))

        fig.add_trace(go.Scatter(mode="markers", x=data.index, y=data.BuySignalPrice, marker_symbol='triangle-up',
                                marker_line_color="#000000", marker_color="#000000", 
                                marker_line_width=2, marker_size=15, name='Buy'))

        fig.add_trace(go.Scatter(mode="markers", x=data.index, y=data.SellSignalPrice, marker_symbol='triangle-down',
                                marker_line_color="#E74C3C", marker_color="#E74C3C", 
                                marker_line_width=2, marker_size=15, name='Sell'))
        fig.show()
        plt.savefig('sma_chart.png')



if __name__ == "__main__":
    sma.movingAVG()