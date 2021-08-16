import requests
from api_data import get_coin_data, get_coinbase_data, sell_quote

def main():
    current_balance_usd, original_balance_usd, transaction_ids, current_balance_crypto = get_coinbase_data()

    profit_loss = sell_quote(current_balance_crypto, transaction_ids)

    print(profit_loss)
    print(original_balance_usd)

    buy_or_sell_calculator(profit_loss,original_balance_usd)
   

def buy_or_sell_calculator(profit_loss, original_balance_usd):
    net = {}
    percent_change = {}
    portfolio_total = 0
    for key_profit, key_original in zip(profit_loss, original_balance_usd):
        net[key_profit] = (float(profit_loss[key_profit]) - original_balance_usd[key_original])
        portfolio_total += net[key_profit]
        percent_change[key_profit] = ((net[key_profit]) / original_balance_usd[key_original]) * 100

    print(net)
    print(percent_change)
    print(portfolio_total)



main()

