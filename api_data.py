from urllib.parse import quote
from requests import Request, Session
from apikey import apikey, coinbase, coinbase_secret, crypto_compare
import json
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from coinbase.wallet.client import Client
import re

def get_coin_data():

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': apikey
    }
    parameters = {
        'slug': 'bitcoin',
        'convert': 'USD'
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

# Should retrieve what crypto and the current balance for that crypto
# Should retrieve what price I bought crypto at 
def get_coinbase_data():
    api_key = coinbase
    api_secret = coinbase_secret
    client = Client(api_key=api_key, api_secret=api_secret)

    total = 0
    accounts = client.get_accounts(limit=100)

    transaction_ids = {}
    for wallet in accounts.data:
        if str(wallet['native_balance']) != 'USD 0.00':
            transaction_ids[str(wallet['name'])] = str(wallet['id'])
            value = str( wallet['native_balance']).replace('USD','')
            total += float(value)
    del transaction_ids['COMP Wallet']
    del transaction_ids['GRT Wallet']

    bought_balance_crypto = {}
    price_conversion_list = []
    original_crypto_usd = {}
    for key in transaction_ids.keys():
        transaction_total = client.get_transactions(transaction_ids[key])
        price_conversion_list.append(key.replace(' Wallet',''))
        for i in range(len(transaction_total['data']) - 1, -1, -1):
            try:
                if transaction_total[i]['details']['header'][0:4] == 'Sold':
                    proportion = float(bought_balance_crypto.get(key)) // float(transaction_total[i]['amount']['amount'])
                    bought_balance_crypto[key] = float(transaction_total[i]['amount']['amount']) + float(bought_balance_crypto.get(key))
                    original_crypto_usd[key] = original_crypto_usd[key] - (original_crypto_usd[key] * (abs(1/proportion)))
                   
                elif transaction_total[i]['details']['header'][0:6] == 'Bought' or transaction_total[i]['details']['header'][0:8] == 'Received':
                    bought_balance_crypto[key] = float(transaction_total[i]['amount']['amount']) + float(bought_balance_crypto.get(key))
                    temp = transaction_total[i]['details']['header']

                    try:
                        new_text = re.findall('(\$\d+\.?\d*)', str(temp))
                        original_crypto_usd[key] = float((new_text[0]).replace('$','')) + float(original_crypto_usd[key])
                    
                    except AttributeError:
                        new_text = ''
                        original_crypto_usd[key] = -1
                   
            except:
                bought_balance_crypto[key] = float(transaction_total[i]['amount']['amount'])
                temp = transaction_total[i]['details']['header']
                try:
                    new_text = re.search('(\$\d+\.?\d*)', temp)
                    original_crypto_usd[key] = float((new_text[0]).replace('$',''))
                except AttributeError:
                    new_text = ''
                    original_crypto_usd[key] = -1
            

    current_crypto_usd = price_conversion(','.join(price_conversion_list))
    balance_usd = {}
    for key_crypto, key_balance in zip(current_crypto_usd.keys(), bought_balance_crypto.keys()):
        balance_usd[key_crypto] = bought_balance_crypto[key_balance] / current_crypto_usd[key_crypto]
   
    return (balance_usd, original_crypto_usd, transaction_ids, bought_balance_crypto)
    
def price_conversion(cryptos):
    key = crypto_compare
    url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=USD&tsyms='+cryptos+'&api_key='+key

    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return data['USD']


def sell_quote(current_balance_crypto, transaction_ids):
    api_key = coinbase
    api_secret = coinbase_secret
    client = Client(api_key=api_key, api_secret=api_secret)

    total_proft_loss = {}
    sell_price = {}
    for keys in  transaction_ids.keys():
        sell = client.sell(transaction_ids[keys],
                   amount=current_balance_crypto[keys],
                   currency=keys.replace(' Wallet', ''),
                   quote=True)
        total_proft_loss[keys] = sell['total']['amount']
        
    return total_proft_loss
    



    


        
