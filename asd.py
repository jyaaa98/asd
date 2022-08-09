from binance.client import Client

client = Client(api_key='dF4p7Br4O3lX4TYU6KWem0S9bWzDcegjGyosjTllPAeARJS5DIeVjAym5aGsuzhI', api_secret='07OhFDjoEpSbG4SWX3SL3mgFHuKck3Xd1i69zcUlY6WWQSSDZvXgUk1LvSJeoGyq')

k = 1.01
btc_usdt = client.get_symbol_ticker(symbol='BTCUSDT')
price = btc_usdt['price']
buy_price = price
sell_price = price
orderId = 0

while True:
    btc = client.get_asset_balance(asset='BTC')
    usdt = client.get_asset_balance(asset='USDT')
    if btc['free'] == usdt['locked']:
        if usdt['free'] == btc['locked']:
            btc_usdt = client.get_symbol_ticker(symbol='BTCUSDT')
            price = btc_usdt['price']
            if price > buy_price:
                order = client.order_limit_sell(symbol='BTCUSDT', quantity=btc['free'], price=price)
                orderId = order['orderId']
                sell_price = price
            elif float(price) < float(buy_price) / k:
                break
        else:
            btc_usdt = client.get_symbol_ticker(symbol='BTCUSDT')
            price = btc_usdt['price']
            if price < sell_price:
                order = client.order_limit_buy(symbol='BTCUSDT', quantity=usdt['free'], price=1)
                orderId = order['orderId']
                buy_price = price
            elif float(price) > float(sell_price) * k:
                break
    else:
        if usdt['free'] == btc['locked']:
            btc_usdt = client.get_symbol_ticker(symbol='BTCUSDT')
            price = btc_usdt['price']
            if price < buy_price:
                client.cancel_order(symbaol='BTCUSDT', orderId=orderId)
                order = client.order_limit_buy(symbol='BTCUSDT', quantity=usdt['free'], price=1)
                orderId = order['orderId']
                buy_price = price
        else:
            btc_usdt = client.get_symbol_ticker(symbol='BTCUSDT')
            price = btc_usdt['price']
            if price > sell_price:
                client.cancel_order(symbaol='BTCUSDT', orderId=orderId)
                order = client.order_limit_sell(symbol='BTCUSDT', quantity=btc['free'], price=price)
                orderId = order['orderId']
                sell_price = price