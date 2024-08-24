from flask import Flask
from datetime import datetime
from flask_cors import CORS
import requests as rq
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():  
    return 'Hello World!'

@app.route('/query/<string:source>/<string:ticker>/<string:interval>')
def query(source ,ticker, interval):
    results = {}
    # Define intervals based on 
    intDict = {'d':'5min',
               'w':'4h',
               'm':'1day',
               'y':'1day'}
    outDict = {'d':'78',
               'w':'42',
               'm':'30',
               'y':'252'}
    formDict = {'d':'%I:%M %p',
                'w':'%m-%d-%Y %I:%M %p',
                'm':'%m-%d-%Y',
                'y':'%m-%d-%Y'}
    resDict = {'d':'%Y-%m-%d %H:%M:%S',
               'w':'%Y-%m-%d %H:%M:%S',
               'm':'%Y-%m-%d',
               'y':'%Y-%m-%d'}
    options=['close', 'high', 'low', 'open']
    chart_Key = os.getenv('KEY')
    news_Key  = os.getenv('NEWSST')
    if source == 'stocks':
        chart_URL = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval={intDict[interval]}&outputsize={outDict[interval]}'
        news_URL  = f'https://api.marketaux.com/v1/news/all?symbols={ticker}&filter_entities=true&api_token={news_Key}'
        info_URL  = f'https://api.twelvedata.com/stocks?symbol={ticker}&exchange=NASDAQ'
    elif source == 'crypto':
        chart_URL = f'https://api.twelvedata.com/time_series?symbol={ticker}/USD&interval={intDict[interval]}&outputsize={outDict[interval]}'
        news_URL  = f'CRYPTO NEWS URL HERE'
        info_URL  = f'INFO URL HERE'
    header={'Authorization':f"apikey {chart_Key}"}
    try:
        chartData = rq.get(chart_URL, headers=header).json()['values']
    except:
        chartData = []
    try:
        newsData  = rq.get(news_URL).json()['data']
        #results['name'] = newsData[0]['name']
    except:
        newsData = []
    try:
        infoData = rq.get(info_URL, headers=header).json()['data'][0]
    except:
        infoData = []
    chartData.reverse()
    for each in chartData:
        each['datetime'] = datetime.strptime(each['datetime'], resDict[interval]).strftime(formDict[interval])
        for op in options:
            each[op] = "{:.2f}".format(float(each[op]))
    results['chartData'] = chartData
    results['newsData']  = newsData
    results['infoData']  = infoData
    return results

@app.route('/tickerList/<string:exchange>')
def tickerList(exchange):
    tickersL = []
    volumeL = []
    special = os.getenv('KEY')
    header={'Authorization':f"apikey {special}"}
    if exchange in ['crypto', 'CRYPTO']:
        url = 'https://api.twelvedata.com/cryptocurrencies'
        response = rq.get(url, headers=header)
        results = response.json()['data']
        for row in results:
            if 'USD' in row['symbol']:
                form = row['symbol'].rstrip('/USD')
                # For some reason the api returns a lot of values with symbols of just "/USD" so I need to check for those and remove them if they exist
                if form != '':
                    tickersL.append(form)
        special = os.getenv('CRYPTORK')
        header={'x-access-token':special}
        url = 'https://api.coinranking.com/v2/coins?orderBy=24hVolume'
        response = rq.get(url, headers=header) 
        volumeL = response.json()['data']['coins']
        for r in volumeL:
            r['price'] = "{:.2f}".format(float(r['price']))
    else:
        url = f'https://api.twelvedata.com/stocks?exchange={exchange}'
        response = rq.get(url, headers=header)
        results = response.json()['data']
        for row in results:
            tickersL.append(row['symbol'])
        special = os.getenv('VOLUME')
        key = f'apikey={special}'
        url = f'https://financialmodelingprep.com/api/v3/stock_market/actives?{key}'
        response = rq.get(url)
        volumeL = response.json()
    results = {'tickers':tickersL, 'volume':volumeL, 'exchange':exchange}
    return results