from api_data import get_coin_data, get_coinbase_data, sell_quote, pushover_notifications


def main():
    current_balance_usd, original_balance_usd, transaction_ids, current_balance_crypto = get_coinbase_data()
    
    currency_symbols = []

    for keys in transaction_ids.keys():
        currency_symbols.append(keys.replace(' Wallet',''))
    print(current_balance_crypto)
    profit_loss = sell_quote(current_balance_crypto, transaction_ids)
    net, percent_change, portfolio_total = buy_or_sell_calculator(profit_loss,original_balance_usd)

    coinmarket_data = get_coin_data(",".join(currency_symbols))
   
    message = ""
    title = ("CY  |"," CB  |","  OB  |", " Net  |", " PC  |", " CPC")

    list_conversion = []
    list_conversion.append([])
    list_conversion[0].extend(title)
    current_balance_usd_round = [round(num, 2) for num in current_balance_usd.values()]
    original_balance_usd_round = [round(num, 2) for num in original_balance_usd.values()]
    net_round = [round(num, 2) for num in net.values()]
    percent_round = [round(num, 2) for num in percent_change.values()]

    for index, key in enumerate(current_balance_usd):
        list_conversion.append([])
        list_conversion[index + 1].append(key)
        list_conversion[index + 1].append(current_balance_usd_round[index])

    for index, key in enumerate(original_balance_usd_round):
        list_conversion[index + 1].append(key)
        list_conversion[index + 1].append(net_round[index])
        list_conversion[index + 1].append(percent_round[index])

    for index, val in enumerate(currency_symbols):
         list_conversion[index +1].append(round(coinmarket_data['data'][val]['quote']['USD']['percent_change_1h'],3))


    for index, strs in enumerate(list_conversion):
        if index != 0:
            message+=(' | '.join(map(str, strs)))
            message+='\n\n'
        elif index == 0:
            message+=('  '.join(map(str, strs)))
            message+='\n'
    message+=("Portfolio Total" +": "+str(round(portfolio_total, 2)))

    pushover_notifications(message)
    
    

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

