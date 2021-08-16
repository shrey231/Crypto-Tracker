import requests
from api_data import get_coin_data, get_coinbase_data, sell_quote

def main():
    current_balance_usd, original_balance_usd, transaction_ids, current_balance_crypto = get_coinbase_data()
    # Compare current and orginal show percent difference and show profits or loss
    # Determine if it is a selling or buying price
    # Also parse coin data to show percent change in current market
    # Figure out database storage - what to store and fix coinbase data extraction
    # It will store the latest transaction data of each currency - if it is the same as before it will not loop through api call
    # it will rather extract data stored in database.
    # If the transactoin is different it will take what is already stored in database and then add newer transactions and store in database


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

