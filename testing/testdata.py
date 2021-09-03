import argparse
from datetime import datetime, timedelta
import json
import asyncio
import time
from dateutil.tz import tzlocal
import requests
from websocket import create_connection

def get_beginning_level_3():
    global beginning_level_3
    beginning_level_3 = requests.get('https://api.pro.coinbase.com/products/ETH-USD/book?level=3').json()

async def get_websocket_data():
    global messages
    global latencies

    messages = []
    count = 0

    URL = "wss://ws-feed.pro.coinbase.com"
    params = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["ETH-USD"]}]
    }
    
    coinbase_websocket = create_connection(URL)
    coinbase_websocket.send(json.dumps(params))

    while True: 
        message =  coinbase_websocket.recv()
        message = json.loads(message)
        messages += [message]
        count += 1
        print(count)
        print(datetime.now(tzlocal()))

        if count == 10:
            get_beginning_level_3()
            return

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_websocket_data())

    global messages
    global latencies
    global beginning_level_3

    first_sequence = beginning_level_3['sequence']
    print(messages)

    with open('testing/messages.json', 'w') as json_file:
        json.dump(messages, json_file, indent=4, sort_keys=True)

    with open('testing/beginning_level_3.json', 'w') as json_file:
        json.dump(beginning_level_3, json_file, indent=4, sort_keys=True)
