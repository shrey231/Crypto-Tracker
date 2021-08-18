import requests
from api_data import get_coin_data, get_coinbase_data, sell_quote, pushover_notifications

def main():
    current_balance_usd, original_balance_usd, transaction_ids, current_balance_crypto = get_coinbase_data()
    
    currency_symbols = []

    for keys in transaction_ids.keys():
        currency_symbols.append(keys.replace(' Wallet',''))

    profit_loss = sell_quote(current_balance_crypto, transaction_ids)
    net, percent_change, portfolio_total = buy_or_sell_calculator(profit_loss,original_balance_usd)

    coinmarket_data = get_coin_data(",".join(currency_symbols))
    for val in currency_symbols:
        print(val, coinmarket_data['data'][val]['quote']['USD']['percent_change_1h'])

    pushover_notifications()
    
    

def buy_or_sell_calculator(profit_loss, original_balance_usd):
    net = {}
    percent_change = {}
    portfolio_total = 0
    for key_profit, key_original in zip(profit_loss, original_balance_usd):
        net[key_profit] = (float(profit_loss[key_profit]) - original_balance_usd[key_original])
        portfolio_total += net[key_profit]
        percent_change[key_profit] = ((net[key_profit]) / original_balance_usd[key_original]) * 100

    return (net, percent_change, portfolio_total)



main()

