import pyupbit, pandas, socket
import hashlib, time, jwt, requests, uuid, json
from urllib.parse import urlencode
import telegram
from telegram.ext import Updater, CommandHandler
import threading
import pymysql

# >>> GLOBAL VARIALBES
address = 'academy'

with open('key', 'r') as f:
    data = json.load(f)

# >>> TELEGRAM
telgm_token, telgm_id = data['telegram']['token'], data['telegram']['chat_id']
bot = telegram.Bot(token=telgm_token)
updater = Updater(token=telgm_token, use_context=True)
dispatcher = updater.dispatcher

# >>> UPBIT API
access_key = data[address]['access']
secret_key = data[address]['secret']
upbit = pyupbit.Upbit(access_key, secret_key)
bitcoin = 'KRW-BIT'
ripple = 'KRW-XRP'

class upbit
def send_message(text):
    bot.sendMessage(chat_id=telgm_id, text=text)

def get_ip():
    print("Host Name ",socket.gethostname())
    print("IP Address(Internal) : ", socket.gethostbyname(socket.gethostname()))
    print("IP Address(External) : ", requests.get("https://api.ipify.org").text)


def get_balance():
    balance = upbit.get_balances()
    s = ""
    for coin in balance:
        currency = coin['currency']
        unit = coin['unit_currency']
        market = unit+'-'+currency
        money = float(coin['balance'])
        rate = 1 if currency == 'KRW' else pyupbit.get_current_price(market)
        s += '{} : {:11,.0f} won\n'.format(currency, money*rate)
        if currency != 'KRW':
            avg_buy_price = float(coin['avg_buy_price'])
            now_price = pyupbit.get_current_price(market)
            s += '             평균매수가: {}\n'.format(avg_buy_price)
            s += '             현재가: {}\n'.format(now_price)
            yields = (now_price - avg_buy_price) / avg_buy_price * 100
            s += '             수익률: {:+.2f}%\n'.format(yields)
            if yields < -20:
                sell(market)
    print(s)
    #send_message(s)
    return s


def get_yesterday_trade_price(market):
    url = 'https://api.upbit.com/v1/candles/days'
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 86400))
    querystring = {'market':market, 'to':date, 'count':'1'}
    response = requests.request('GET', url, params=querystring)
    return float(response.json()[0]['trade_price'])

def get_current_price(market):


def get_precedence_stocks(update, context):
    a = []
    s = ""
    tickers = pyupbit.get_tickers(fiat='KRW')
    for ticker in tickers:
        try:
            current_price = pyupbit.get_current_price(ticker)
            yesterday_price = get_yesterday_trade_price(ticker)
        except:
            s += '{} is failed\n'.format(ticker)
            continue
        if yesterday_price == None or current_price is None:
            continue
        percent = (current_price - yesterday_price) / yesterday_price * 100
        step = int(percent)
    print(s)
    # a.sort(key=lambda x:x[1], reverse=True)
    # for i in a:
    #     s += '{:8s} is increase up to {:.1f}%\n'.format(i[0], i[1]*100)
    # print(s)
    # send_message(s)

def request_headers(query=None):
        payload = {"access_key": access_key, "nonce": str(uuid.uuid4())}

        if query is not None:
            m = hashlib.sha512()
            m.update(urlencode(query).encode())
            query_hash = m.hexdigest()
            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = "SHA512"

        jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorization_token}
        return headers


def sell(market, price=None, volume=None, order_type='limit'):
    ### order_type: limit, market
    if volume == None:
        volume = max_buy_coin(market)
    if price == None:
        price = pyupbit.get_current_price(market)
    url = 'https://api.upbit.com/v1/orders'
    query = {'market':market, 'side':'ask', 'volume':volume, 'price':price, 'ord_type':order_type,}
    headers = request_headers(query)
    res = requests.post(url, params=query, headers=headers)
    print('sell {} {} coins in {}won'.format(market, volume, price))

def max_buy_coin(market):
    url = 'https://api.upbit.com/v1/orders/chance'
    query = {'market':market}
    headers = request_headers(query)
    res = requests.get(url, params=query, headers=headers)
    res = res.json()['bid_account']['balance']
    return float(res)/pyupbit.get_current_price(market)

def max_sell_coin(market):
    url = 'https://api.upbit.com/v1/orders/chance'
    query = {'market':market}
    headers = request_headers(query)
    res = requests.get(url, params=query, headers=headers)
    res = res.json()['ask_account']['balance']
    return float(res)/pyupbit.get_current_price(market)

def buy(market, price, volume, order_type='limit'):
    if volume == None:
        pass
    ### order_type: limit, price
    url = 'https://api.upbit.com/v1/orders'
    query = {'market':market, 'side':'bid', 'volume':volume, 'price':price, 'ord_type':order_type,}
    headers = request_headers(query)
    res = requests.post(url, params=query, headers=headers)
    print(res.json())

print('#'*80)

if __name__ == '__main__':

    #send_message('d2h10s upbit macro is opened')
    #get_ip()
    #get_precedence_stocks()
    
    # blance_handler = CommandHandler('balance', get_balance)
    # recent_handler = CommandHandler('recent', get_precedence_stocks)

    # dispatcher.add_handler(blance_handler)
    # dispatcher.add_handler(recent_handler)
    # updater.start_polling()
    # updater.idle()
    while True:
        get_balance()
    #send_message('d2h10s upbit macro is closed')


print('#'*80)
