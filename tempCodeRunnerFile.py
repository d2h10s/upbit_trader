import pyupbit, pandas, socket
import hashlib, time, jwt, requests, uuid, json
from urllib.parse import urlencode
import telegram
from telegram.ext import Updater, CommandHandler
import threading
import pymysql

# >>> GLOBAL VARIALBES
address = 'lab_key'

with open('key', 'r') as f:
    json_data = json.load(f)

# >>> TELEGRAM
telgm_token, telgm_id = json_data['telegram_token'], json_data['telegram_id']
bot = telegram.Bot(token=telgm_token)
updater = Updater(token=telgm_token, use_context=True)
dispatcher = updater.dispatcher

# >>> UPBIT API

access_key = json_data[address]['access']
secret_key = json_data[address]['secret']
upbit = pyupbit.Upbit((access_key, secret_key))
bitcoin = 'KRW-BIT'
ripple = 'KRW-XRP'


def send_message(text):
    bot.sendMessage(chat_id=telgm_id, text=text)

def get_ip():
    print("Host Name ",socket.gethostname())
    print("IP Address(Internal) : ", socket.gethostbyname(socket.gethostname()))
    print("IP Address(External) : ", requests.get("https://api.ipify.org").text)


def get_balance(update, context):
    balance = upbit.get_balances()
    s = ""
    for coin in balance:
        currency = coin['currency']
        unit = coin['unit_currency']
        money = float(coin['balance'])
        rate = 1 if currency == 'KRW' else pyupbit.get_current_price(unit+'-'+currency)
        s += '{} : {:11,.0f} won\n'.format(currency, money*rate)
        if currency != 'KRW':
            avg_buy_price = float(coin['avg_buy_price'])
            now_price = pyupbit.get_current_price(unit+'-'+currency)
            s += '             평균매수가: {}\n'.format(avg_buy_price)
            s += '             현재가: {}\n'.format(now_price)
            yields = (now_price - avg_buy_price) / avg_buy_price * 100
            s += '             수익률: {:+.2f}%\n'.format(yields)
    print(s)
    send_message(s)
    return s


def get_yesterday_trade_price(market):
    url = 'https://api.upbit.com/v1/candles/days'
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 86400))
    querystring = {'market':market, 'to':date, 'count':'1'}
    response = requests.request('GET', url, params=querystring)
    return float(response.json()[0]['trade_price'])


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



print('#'*80)

if __name__ == '__main__':
    send_message('d2h10s upbit macro is opened')
    get_ip()
    get_balance('a','a')
    get_precedence_stocks('a','a')
    # blance_handler = CommandHandler('balance', get_balance)
    # recent_handler = CommandHandler('recent', get_precedence_stocks)

    # dispatcher.add_handler(blance_handler)
    # dispatcher.add_handler(recent_handler)
    # updater.start_polling()
    # updater.idle()
    while True:
        get_balance(1, 1)
    send_message('d2h10s upbit macro is closed')


print('#'*80)
