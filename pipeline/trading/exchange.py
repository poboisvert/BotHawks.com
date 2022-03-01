import time

import hmac
import hashlib
import base64
from requests.auth import AuthBase
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

class CoinbaseExchangeAuthentication(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        message = message.encode('utf-8')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        request.headers.update({
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
        })
        return request

exchange_api_url = 'https://api.pro.coinbase.com/'

exchange_auth = CoinbaseExchangeAuthentication(os.getenv("COINBASE_EXCHANGE_API_KEY"), os.getenv("COINBASE_EXCHANGE_API_SECRET"),
                                               os.getenv("COINBASE_EXCHANGE_API_PASSPHRASE"))