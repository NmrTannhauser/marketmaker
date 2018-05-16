from __future__ import print_function
import requests, json
import threading
import time
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pywaves as pw
import datetime
import math
import logging
import os
import config
import telebot  #Используются API телеграма
from test import getPK
import logging


logging.basicConfig(filename='server.log', level=logging.INFO)

bot = telebot.TeleBot(config.token)

#Необходимо создать канал и добавить в него администратором бота (токен бота в config.py)
CHANNEL_NAME = '@cryptomixtest'


def send_new_posts(message): #Функция отправки в канал
    bot.send_message(CHANNEL_NAME, message)
    return

class RepeatedTimer(object):
  def __init__(self, interval, function):
    self._timer = None
    self.interval = interval
    self.function = function
    self.is_running = False
    self.next_call = time.time()
    self.start()
  def _run(self):
    self.is_running = False
    self.start()
    self.function()
  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True
  def stop(self):
    self._timer.cancel()
    self.is_running = False

class market:
    def __init__(self):
      self.log_file = "bot.log"
      self.node = "https://nodes.wavesnodes.com"
      self.chain = "mainnet"
      self.matcher = "https://nodes.wavesnodes.com"
      self.order_fee = 0.003 * 10 ** 8
      self.order_lifetime = 86400  # 29 days
      self.private_key = key
      self.amount_asset_id = "CFD3qQq9XJ3WXZ3WNDC3we3CGLwPZ5EuNhphRvDH55DF"
      self.price_asset_id_btc = "8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS"
      self.price_asset_id_eth = "474jTeYx2r2Va35794tCScAXWJG9hU2HcgxzMowaZUnu"
      self.price_asset_id_waves = ''
      self.amount_asset = pw.Asset(self.amount_asset_id)
      self.price_asset_btc = pw.Asset(self.price_asset_id_btc)
      self.price_asset_eth = pw.Asset(self.price_asset_id_eth)
      self.price_asset_waves = pw.Asset(self.price_asset_id_waves)

def mixorder(type,pair,amount,price):
    bid_amount = int(amount * 10 ** pw.WAVES.decimals)
    bid_price = int(price * 10 ** pw.WAVES.decimals)
    if (type == 'buy'):
        id = my_address.buy(assetPair=pair,amount = bid_amount, price = bid_price)
    else:
        id = my_address.sell(assetPair=pair,amount = bid_amount, price = bid_price)
    return id.orderId
key = getPK()
market = market()
pw.setNode(node=market.node, chain=market.chain)
pw.setMatcher(node=market.matcher)
my_address = pw.Address(privateKey=market.private_key)
cryptomix_btc = pw.AssetPair(market.amount_asset, market.price_asset_btc)
cryptomix_eth = pw.AssetPair(market.amount_asset, market.price_asset_eth)
cryptomix_waves = pw.AssetPair(market.amount_asset, market.price_asset_waves)
BTCprice = 0
ETHprice = 0
WAVESprice = 0

def getprices():
    SCOPES = "https://www.googleapis.com/auth/spreadsheets.readonly"
    store = file.Storage("/home/projects/market/credentials.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("/home/projects/market/client_secret.json", SCOPES)
        creds = tools.run_flow(flow, store)
    service = build("sheets", "v4", http=creds.authorize(Http()))
    SPREADSHEET_ID = "15RUQce2liQe5ojMzgynm8ghs3E7fwwkf5gm3mMyGV_8"
    RANGE_NAME = "Portfolio!C6:Q6"
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    pricelist = result.get("values", [])
    try:
        BTCprice = float(pricelist[0][0].replace(',','.'))
        ETHprice = float(pricelist[0][9].replace(',','.'))
        WAVESprice = float(pricelist[0][12].replace(',','.'))
    except Exception as e:
        logging.error(e)
        BTCprice = 0
        ETHprice = 0
        WAVESprice = 0
    with open('prices.txt','w') as prf:
        print(BTCprice, file=prf)
        print(ETHprice, file=prf)
        print(WAVESprice, file=prf)

try:
    BTCtradeallow = 0
    ETHtradeallow = 0
    WAVEStradeallow = 0
    buyBTCtime = 0
    buyETHtime = 0
    buyWAVEStime = 0
    sellBTCtime = 0
    sellETHtime = 0
    sellWAVEStime = 0
    oldBTCprice = 0
    oldETHprice = 0
    oldWAVESprice = 0
    newBTCprice = 0
    newETHprice = 0
    newWAVESprice = 0
    timechecktime = time.time()
    buyOrderBTC = ''
    buyOrderETH = ''
    buyOrderWAVES = ''
    sellOrderBTC = ''
    sellOrderETH = ''
    sellOrderWAVES = ''
    res = requests.get('http://127.0.0.1:8000/json/').json()
    status = res['status']
    timeprice = res['TimePrice']
    a = RepeatedTimer(timeprice,getprices)
    with open('prices.txt','r') as prf:
        pricesff = prf.read()
    listpr = pricesff.split('\n')
    BTCprice = float(listpr[0])
    ETHprice = float(listpr[1])
    WAVESprice = float(listpr[2])
    BTCtradeallow = 0 if (BTCprice == 0) else 1
    ETHtradeallow = 0 if (ETHprice == 0) else 1
    WAVEStradeallow = 0 if (WAVESprice == 0) else 1
    oldBTCprice = BTCprice
    oldETHprice = ETHprice
    oldWAVESprice = WAVESprice
    newBTCprice = BTCprice
    newETHprice = ETHprice
    newWAVESprice = WAVESprice
    oldstatus = res['status']
    timepricetime = time.time()
    while True:
        try:
            get = requests.get('http://127.0.0.1:8000/json/').json()
            status = get['status']
            timeprice = get['TimePrice']
            a.interval = timeprice
            if (time.time()-timepricetime>timeprice):    #получение цен и проверка возможности торгов
                with open('prices.txt','r') as prf:
                    pricesff = prf.read()
                listpr = pricesff.split('\n')
                BTCprice = float(listpr[0])
                ETHprice = float(listpr[1])
                WAVESprice = float(listpr[2])
                timepricetime = time.time()
                if (BTCprice == 0 or abs(newBTCprice-BTCprice)>get['ThreshHold']):
                    BTCtradeallow = 0
                    send_new_posts('цена ВТС = 0 или резкое изменение цены')
                    #сообщение в телеграмм
                    if (buyBTCtime or sellBTCtime):
                        my_address.cancelOpenOrders(cryptomix_btc)
                        buyBTCtime = 0
                        sellBTCtime = 0
                else:
                    BTCtradeallow = 1
                    newBTCprice = BTCprice
                if (ETHprice == 0 or abs(newETHprice-ETHprice)>get['ThreshHold']):
                    ETHtradeallow = 0
                    send_new_posts('цена ETH = 0 или резкое изменение цены')
                    #сообщение в телеграмм
                    if (buyETHtime or sellETHtime):
                        my_address.cancelOpenOrders(cryptomix_eth)
                        buyETHtime = 0
                        sellETHtime = 0
                else:
                    ETHtradeallow = 1
                    newETHprice = ETHprice
                if (WAVESprice == 0 or abs(newWAVESprice-WAVESprice)>get['ThreshHold']):
                    WAVEStradeallow = 0
                    send_new_posts('цена WAVES = 0 или резкое изменение цены')
                    #сообщение в телеграмм
                    if (buyWAVEStime or sellWAVEStime):
                        my_address.cancelOpenOrders(cryptomix_waves)
                        buyWAVEStime = 0
                        sellWAVEStime = 0
                else:
                    WAVEStradeallow = 1
                    newWAVESprice = WAVESprice

            if (status):                      #робот включен
                if (oldstatus != status):               #только что включился
                    if (get['Buy']['amountBTCtoken'] and BTCtradeallow):
                        BTCpricetotal = newBTCprice*(1-get['Buy']['percentBTC']/100) if get['Buy']['percentBTC'] else newBTCprice
                        buyOrderBTC = mixorder('buy',cryptomix_btc,get['Buy']['amountBTCtoken'],BTCpricetotal)
                        buyBTCtime = time.time()

                    if (get['Buy']['amountETHtoken'] and ETHtradeallow):
                        ETHpricetotal = newETHprice*(1-get['Buy']['percentETH']/100) if get['Buy']['percentETH'] else newETHprice
                        buyOrderETH = mixorder('buy',cryptomix_eth,get['Buy']['amountETHtoken'],ETHpricetotal)
                        buyETHtime = time.time()

                    if (get['Buy']['amountWAVEStoken'] and WAVEStradeallow):
                        WAVESpricetotal = newWAVESprice*(1-get['Buy']['percentWAVES']/100) if get['Buy']['percentWAVES'] else newWAVESprice
                        buyOrderWAVES = mixorder('buy',cryptomix_waves,get['Buy']['amountWAVEStoken'],WAVESpricetotal)
                        buyWAVEStime = time.time()

                    if (get['Sell']['amountBTCtoken'] and BTCtradeallow):
                        BTCpricetotal = newBTCprice*(1+get['Sell']['percentBTC']/100) if get['Sell']['percentBTC'] else newBTCprice
                        sellOrderBTC = mixorder('sell',cryptomix_btc,get['Sell']['amountBTCtoken'],BTCpricetotal)
                        sellBTCtime = time.time()

                    if (get['Sell']['amountETHtoken'] and ETHtradeallow):
                        ETHpricetotal = newETHprice*(1+get['Sell']['percentETH']/100) if get['Sell']['percentETH'] else newETHprice
                        sellOrderETH = mixorder('sell',cryptomix_eth,get['Sell']['amountETHtoken'],ETHpricetotal)
                        sellETHtime = time.time()

                    if (get['Sell']['amountWAVEStoken'] and WAVEStradeallow):
                        WAVESpricetotal = newWAVESprice*(1+get['Sell']['percentWAVES']/100) if get['Sell']['percentWAVES'] else newWAVESprice
                        sellOrderWAVES = mixorder('sell',cryptomix_waves,get['Sell']['amountWAVEStoken'],WAVESpricetotal)
                        sellWAVEStime = time.time()

                else:                                           #обычный режим работы
                    if (get['Buy']['amountBTCtoken'] and ((oldBTCprice != newBTCprice) or  not(buyBTCtime)) and BTCtradeallow):
                        if (len(buyOrderBTC)>5):
                            my_address.cancelOrderByID(cryptomix_btc, buyOrderBTC)
                            buyBTCtime = 0
                        BTCpricetotal = newBTCprice*(1-get['Buy']['percentBTC']/100) if get['Buy']['percentBTC'] else newBTCprice
                        buyOrderBTC = mixorder('buy',cryptomix_btc,get['Buy']['amountBTCtoken'],BTCpricetotal)
                        buyBTCtime = time.time()


                    if (get['Buy']['amountETHtoken'] and ((oldETHprice != newETHprice) or  not(buyETHtime)) and ETHtradeallow):
                        if (len(buyOrderETH)>5):
                            my_address.cancelOrderByID(cryptomix_eth, buyOrderETH)
                            buyETHtime = 0
                        ETHpricetotal = newETHprice*(1-get['Buy']['percentETH']/100) if get['Buy']['percentETH'] else newETHprice
                        buyOrderETH = mixorder('buy',cryptomix_eth,get['Buy']['amountETHtoken'],ETHpricetotal)
                        buyETHtime = time.time()


                    if (get['Buy']['amountWAVEStoken'] and ((oldWAVESprice != newWAVESprice) or  not(buyWAVEStime)) and WAVEStradeallow):
                        if (len(buyOrderWAVES)>5):
                            my_address.cancelOrderByID(cryptomix_waves, buyOrderWAVES)
                            buyWAVEStime = 0
                        WAVESpricetotal = newWAVESprice*(1-get['Buy']['percentWAVES']/100) if get['Buy']['percentWAVES'] else newWAVESprice
                        buyOrderWAVES = mixorder('buy',cryptomix_waves,get['Buy']['amountWAVEStoken'],WAVESpricetotal)
                        buyWAVEStime = time.time()


                    if (get['Sell']['amountBTCtoken'] and ((oldBTCprice != newBTCprice) or  not(sellBTCtime)) and BTCtradeallow):
                        if (len(sellOrderBTC)>5):
                            my_address.cancelOrderByID(cryptomix_btc, sellOrderBTC)
                            sellBTCtime = 0
                        BTCpricetotal = newBTCprice*(1+get['Sell']['percentBTC']/100) if get['Sell']['percentBTC'] else newBTCprice
                        sellOrderBTC = mixorder('sell',cryptomix_btc,get['Sell']['amountBTCtoken'],BTCpricetotal)
                        sellBTCtime = time.time()


                    if (get['Sell']['amountETHtoken'] and ((oldETHprice != newETHprice) or  not(sellETHtime)) and ETHtradeallow):
                        if (len(sellOrderETH)>5):
                            my_address.cancelOrderByID(cryptomix_eth, sellOrderETH)
                            sellETHtime = 0
                        ETHpricetotal = newETHprice*(1+get['Sell']['percentETH']/100) if get['Sell']['percentETH'] else newETHprice
                        sellOrderETH = mixorder('sell',cryptomix_eth,get['Sell']['amountETHtoken'],ETHpricetotal)
                        sellETHtime = time.time()


                    if (get['Sell']['amountWAVEStoken'] and ((oldWAVESprice != newWAVESprice) or  not(sellWAVEStime)) and WAVEStradeallow):
                        if (len(sellOrderWAVES)>5):
                            my_address.cancelOrderByID(cryptomix_waves, sellOrderWAVES)
                            sellWAVEStime = 0
                        WAVESpricetotal = newWAVESprice*(1+get['Sell']['percentWAVES']/100) if get['Sell']['percentWAVES'] else newWAVESprice
                        sellOrderWAVES = mixorder('sell',cryptomix_waves,get['Sell']['amountWAVEStoken'],WAVESpricetotal)
                        sellWAVEStime = time.time()

                    if (get['Buy']['amountBTCtoken'] == 0 and buyBTCtime):
                        my_address.cancelOrderByID(cryptomix_btc, buyOrderBTC)
                        buyBTCtime = 0
                        buyOrderBTC = ''

                    if (get['Buy']['amountETHtoken'] == 0 and buyETHtime):
                        my_address.cancelOrderByID(cryptomix_eth, buyOrderETH)
                        buyETHtime = 0
                        buyOrderETH = ''

                    if (get['Buy']['amountWAVEStoken'] == 0 and buyWAVEStime):
                        my_address.cancelOrderByID(cryptomix_waves, buyOrderWAVES)
                        buyWAVEStime = 0
                        buyOrderWAVES = ''

                    if (get['Sell']['amountBTCtoken'] == 0 and sellBTCtime):
                        my_address.cancelOrderByID(cryptomix_btc, buyOrderBTC)
                        sellBTCtime = 0
                        buyOrderBTC = ''

                    if (get['Sell']['amountETHtoken'] == 0 and sellETHtime):
                        my_address.cancelOrderByID(cryptomix_eth, buyOrderETH)
                        sellETHtime = 0
                        buyOrderETH = ''

                    if (get['Sell']['amountWAVEStoken'] == 0 and sellWAVEStime):
                        my_address.cancelOrderByID(cryptomix_waves, buyOrderWAVES)
                        sellWAVEStime = 0
                        buyOrderWAVES = ''
                #конец выставления ордеров
                if (get['BuyBack']['Status']):         #работаем с байбэками
                    if (sellBTCtime and get['BuyBack']['BTC'] and BTCtradeallow and time.time()-sellBTCtime>get['BuyBack']['Time']):
                        BTCpricetotal = newBTCprice*(1+get['Sell']['percentBTC']/100) if get['Sell']['percentBTC'] else newBTCprice
                        buybackOrderBTC = mixorder('buy',cryptomix_btc,get['BuyBack']['BTC'],BTCpricetotal)
                        my_address.cancelOrderByID(cryptomix_btc, buybackOrderBTC)
                        sellBTCtime = 0
                    if (sellETHtime and get['BuyBack']['ETH'] and ETHtradeallow and time.time()-sellETHtime>get['BuyBack']['Time']):
                        ETHpricetotal = newETHprice*(1+get['Sell']['percentETH']/100) if get['Sell']['percentETH'] else newETHprice
                        buybackOrderETH = mixorder('buy',cryptomix_eth,get['BuyBack']['ETH'],ETHpricetotal)
                        my_address.cancelOrderByID(cryptomix_eth, buybackOrderETH)
                        sellETHtime = 0
                    if (sellWAVEStime and get['BuyBack']['WAVES'] and WAVEStradeallow and time.time()-sellWAVEStime>get['BuyBack']['Time']):
                        WAVESpricetotal = newWAVESprice*(1+get['Sell']['percentWAVES']/100) if get['Sell']['percentWAVES'] else newWAVESprice
                        buybackOrderWAVES = mixorder('buy',cryptomix_waves,get['BuyBack']['WAVES'],WAVESpricetotal)
                        my_address.cancelOrderByID(cryptomix_waves, buybackOrderWAVES)
                        sellWAVEStime = 0
                #конец байбэков
                if (get['TimeCheck'] and time.time()-timechecktime>get['TimeCheck']):             #Проверка объемов ордеров
                    timechecktime = time.time()
                    if (len(sellOrderBTC)>5 and BTCtradeallow):
                        order = pw.Order(sellOrderBTC, cryptomix_btc)
                        order_status = order.status()
                        if (order_status['status'] == 'PartiallyFilled'):
                            my_address.cancelOrderByID(cryptomix_btc, sellOrderBTC)
                            BTCpricetotal = newBTCprice*(1+get['Sell']['percentBTC']/100) if get['Sell']['percentBTC'] else newBTCprice
                            sellOrderBTC = mixorder('sell',cryptomix_btc,get['Sell']['amountBTCtoken'],BTCpricetotal)
                            sellBTCtime = time.time()
                    if (len(sellOrderETH)>5 and ETHtradeallow):
                        order = pw.Order(sellOrderETH, cryptomix_eth)
                        order_status = order.status()
                        if (order_status['status'] == 'PartiallyFilled'):
                            my_address.cancelOrderByID(cryptomix_eth, sellOrderETH)
                            ETHpricetotal = newETHprice*(1+get['Sell']['percentETH']/100) if get['Sell']['percentETH'] else newETHprice
                            sellOrderETH = mixorder('sell',cryptomix_eth,get['Sell']['amountETHtoken'],ETHpricetotal)
                            sellETHtime = time.time()
                    if (len(sellOrderWAVES)>5 and WAVEStradeallow):
                        order = pw.Order(sellOrderWAVES, cryptomix_waves)
                        order_status = order.status()
                        if (order_status['status'] == 'PartiallyFilled'):
                            my_address.cancelOrderByID(cryptomix_waves, sellOrderWAVES)
                            WAVESpricetotal = newWAVESprice*(1+get['Sell']['percentWAVES']/100) if get['Sell']['percentWAVES'] else newWAVESprice
                            sellOrderWAVES = mixorder('sell',cryptomix_waves,get['Sell']['amountWAVEStoken'],WAVESpricetotal)
                            sellWAVEStime = time.time()
                    if (len(buyOrderBTC)>5 and BTCtradeallow):
                        order = pw.Order(buyOrderBTC, cryptomix_btc)
                        order_status = order.status()
                        if (order_status['status'] == 'PartiallyFilled'):
                            my_address.cancelOrderByID(cryptomix_btc, buyOrderBTC)
                            BTCpricetotal = newBTCprice*(1-get['Buy']['percentBTC']/100) if get['Buy']['percentBTC'] else newBTCprice
                            buyOrderBTC = mixorder('buy',cryptomix_btc,get['Buy']['amountBTCtoken'],BTCpricetotal)
                            buyBTCtime = time.time()
                    if (len(buyOrderETH)>5 and ETHtradeallow):
                        order = pw.Order(buyOrderETH, cryptomix_eth)
                        order_status = order.status()
                        if (order_status['status'] == 'PartiallyFilled'):
                            my_address.cancelOrderByID(cryptomix_eth, buyOrderETH)
                            ETHpricetotal = newETHprice*(1-get['Buy']['percentETH']/100) if get['Buy']['percentETH'] else newETHprice
                            buyOrderETH = mixorder('buy',cryptomix_eth,get['Buy']['amountETHtoken'],ETHpricetotal)
                            buyETHtime = time.time()
                    if (len(buyOrderWAVES)>5 and WAVEStradeallow):
                        order = pw.Order(buyOrderWAVES, cryptomix_waves)
                        order_status = order.status()
                        if (order_status['status'] == 'PartiallyFilled'):
                            my_address.cancelOrderByID(cryptomix_waves, buyOrderWAVES)
                            WAVESpricetotal = newWAVESprice*(1-get['Buy']['percentWAVES']/100) if get['Buy']['percentWAVES'] else newWAVESprice
                            buyOrderWAVES = mixorder('buy',cryptomix_waves,get['Buy']['amountWAVEStoken'],WAVESpricetotal)
                            buyWAVEStime = time.time()
                #конец проверки объемов

            else:
                if (oldstatus != status):
                    a.stop()
                    if (len(buyOrderBTC)>5):
                        my_address.cancelOrderByID(cryptomix_btc, buyOrderBTC)
                        buyBTCtime = 0
                        buyOrderBTC = ''
                    if (len(buyOrderETH)>5):
                        my_address.cancelOrderByID(cryptomix_eth, buyOrderETH)
                        buyETHtime = 0
                        buyOrderETH = ''
                    if (len(buyOrderWAVES)>5):
                        my_address.cancelOrderByID(cryptomix_waves, buyOrderWAVES)
                        buyWAVEStime = 0
                        buyOrderWAVES = ''
                    if (len(sellOrderBTC)>5):
                        my_address.cancelOrderByID(cryptomix_btc, sellOrderBTC)
                        sellBTCtime = 0
                        sellOrderBTC = ''
                    if (len(sellOrderETH)>5):
                        my_address.cancelOrderByID(cryptomix_eth, sellOrderETH)
                        sellETHtime = 0
                        sellOrderETH = ''
                    if (len(sellOrderWAVES)>5):
                        my_address.cancelOrderByID(cryptomix_waves, sellOrderWAVES)
                        sellWAVEStime = 0
                        sellOrderWAVES = ''
            oldstatus = status
            oldBTCprice = newBTCprice
            oldETHprice = newETHprice
            oldWAVESprice = newWAVESprice
            time.sleep(3)

        except Exception as e1:
            logging.error(e)
            if (len(buyOrderBTC)>5):
                my_address.cancelOrderByID(cryptomix_btc, buyOrderBTC)
                buyBTCtime = 0
                buyOrderBTC = ''
            if (len(buyOrderETH)>5):
                my_address.cancelOrderByID(cryptomix_eth, buyOrderETH)
                buyETHtime = 0
                buyOrderETH = ''
            if (len(buyOrderWAVES)>5):
                my_address.cancelOrderByID(cryptomix_waves, buyOrderWAVES)
                buyWAVEStime = 0
                buyOrderWAVES = ''
            if (len(sellOrderBTC)>5):
                my_address.cancelOrderByID(cryptomix_btc, sellOrderBTC)
                sellBTCtime = 0
                sellOrderBTC = ''
            if (len(sellOrderETH)>5):
                my_address.cancelOrderByID(cryptomix_eth, sellOrderETH)
                sellETHtime = 0
                sellOrderETH = ''
            if (len(sellOrderWAVES)>5):
                my_address.cancelOrderByID(cryptomix_waves, sellOrderWAVES)
                sellWAVEStime = 0
                sellOrderWAVES = ''
except Exception as e:
    logging.error(e)
    if (buyBTCtime or sellBTCtime):
        my_address.cancelOpenOrders(cryptomix_btc)
        buyBTCtime = 0
        buyOrderBTC = ''
        sellBTCtime = 0
        sellOrderBTC = ''

    if (buyETHtime or sellETHtime):
        my_address.cancelOpenOrders(cryptomix_eth)
        buyETHtime = 0
        buyOrderETH = ''
        sellETHtime = 0
        sellOrderETH = ''

    if (buyWAVEStime or sellWAVEStime):
        my_address.cancelOpenOrders(cryptomix_waves)
        buyWAVEStime = 0
        buyOrderWAVES = ''
        sellWAVEStime = 0
        sellOrderWAVES = ''
