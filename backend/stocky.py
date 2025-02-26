import os
from datetime import datetime

import requests
from flask import Flask
from flask_cors import CORS
from twelvedata import TDClient

td = TDClient(apikey=os.getenv('KEY'))
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

@app.route('/')
def hello():  
    return 'Hello World!'

@app.route('/query/<string:source>/<string:ticker>/<string:interval>')
def query(source ,ticker, interval):
    results = {}
    # Define intervals based on 
    int_dict = {'d':'5min',
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
        # Depreciated
        #chart_url = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval={int_dict[interval]}&outputsize={outDict[interval]}'
        news_url  = f'https://api.marketaux.com/v1/news/all?symbols={ticker}&filter_entities=true&api_token={news_Key}'
        info_url  = f'https://api.twelvedata.com/stocks?symbol={ticker}&exchange=NASDAQ'
    elif source == 'crypto':
        # Depreciated
        # chart_url = f'https://api.twelvedata.com/time_series?symbol={ticker}/USD&interval={int_dict[interval]}&outputsize={outDict[interval]}'
        ticker = ticker + '/USD'
        news_url  = f'CRYPTO NEWS url HERE'
        info_url  = f'INFO url HERE'
    header={'Authorization':f"apikey {chart_Key}"}
    try:
        chartData = td.time_series(
            symbol=ticker,
            interval=int_dict[interval],
            outputsize=outDict[interval]
        ).as_json()
        chartData = list(reversed(chartData))
    except :
        chartData = []
    try:
        newsData  = requests.get(news_url).json()['data']
    except:
        newsData = []
    try:
        infoData = requests.get(info_url, headers=header).json()['data'][0]
    except:
        infoData = []
    # DEPRECIATED chartData.reverse()
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
    volume_list = []
    special = os.getenv('KEY')
    header={'Authorization':f"apikey {special}"}
    if exchange in ['crypto', 'CRYPTO']:
        url = 'https://api.twelvedata.com/cryptocurrencies'
        response = requests.get(url, headers=header)
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
        response = requests.get(url, headers=header) 
        volume_list = response.json()['data']['coins']
        for r in volume_list:
            r['price'] = "{:.2f}".format(float(r['price']))
    else:
        url = f'https://api.twelvedata.com/stocks?exchange={exchange}'
        response = requests.get(url, headers=header)
        results = response.json()['data']
        for row in results:
            tickersL.append(row['symbol'])
        special = os.getenv('VOLUME')
        key = f'apikey={special}'
        url = f'https://financialmodelingprep.com/api/v3/stock_market/actives?{key}'
        response = requests.get(url)
        volume_list = response.json()
    results = {'tickers':tickersL, 'volume':volume_list, 'exchange':exchange}
    return results

@app.route('/refreshGraph/<string:source>/<string:ticker>/<string:interval>')
def refreshGraph(source ,ticker, interval):
    results = {}
    chart_Key = os.getenv('KEY')
    # Define intervals based on 
    int_dict = {'d':'5min',
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
    #DEPRECIATED
    #chart_url = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval={int_dict[interval]}&outputsize={outDict[interval]}'
    #header={'Authorization':f"apikey {chart_Key}"}
    try:
        chartData = td.time_series(
            symbol=ticker,
            interval=int_dict[interval],
            outputsize=outDict[interval]
        ).as_json()
        chartData = list(reversed(chartData))
        #chartData = requests.get(chart_url, headers=header).json()['values']
    except:
        chartData = []
    for each in chartData:
        each['datetime'] = datetime.strptime(each['datetime'], resDict[interval]).strftime(formDict[interval])
        for op in options:
            each[op] = "{:.2f}".format(float(each[op]))
    return chartData

@app.route('/homepage/<string:source>/')
def homePage(source):
    retDat = {'news': [], 'data': []}
    options=['close', 'high', 'low', 'open']
    chartData = []
    newsData = []
    if source in ('stocks', 'Stocks'):
        news_Key = os.getenv('NEWSST')
        news_url  = f'https://api.marketaux.com/v1/news/all?must_have_entities=true&industries=Financial&countries=US&api_token={news_Key}'
        try:
            newsData  = requests.get(news_url).json()['data']
        except:
            pass
        try:
            chartData.append({
                'Title':'Invesco QQQ Trust', 
                'Data': 
                    list(reversed(td.time_series(
                        symbol="QQQ",
                        interval="5min",
                        outputsize=78
                    ).as_json()))
            })
        except:
            pass
        try:
            chartData.append({
                'Title':'S&P 500', 
                'Data': 
                    list(reversed(td.time_series(
                        symbol="SPY",
                        interval="5min",
                        outputsize=78
                    ).as_json()))
            })
        except:
            pass
        try:
            chartData.append({
                'Title':'NASDAQ Composite', 
                'Data': 
                    list(reversed(td.time_series(
                        symbol="COMP",
                        interval="5min",
                        outputsize=78
                    ).as_json()))
            })
        except:
            pass
        '''
        chartData = [
            {'Title':'Invesco QQQ Trust', 'Data': qqq,  'Fill': '#04ff00' if qqq[0]['close'] < qqq[-1]['close']   else '#ff0008'},
            {'Title':'S&P 500',           'Data': spy,  'Fill': '#04ff00' if spy[0]['close'] < spy[-1]['close']   else '#ff0008'},
            {'Title':'NASDAQ Composite',  'Data': comp, 'Fill': '#04ff00' if comp[0]['close'] < comp[-1]['close'] else '#ff0008'}
        ]
        '''
    if source in ('crypto', 'Crypto'):
        news_Key = os.getenv('CRPNWS')
        news_url  = f"https://gnews.io/api/v4/search?q=cryptocurrency&lang=en&country=us&max=3&apikey={news_Key}"
        try:
            newsData  = requests.get(news_url).json()['articles']
            for each in newsData:
                each['image_url'] = each.pop('image')
        except:
            pass
        try:
            chartData.append({
                'Title':'Bitcoin', 
                'Data': 
                    list(reversed(td.time_series(
                        symbol="BTC/USD",
                        interval="5min",
                        outputsize=78
                    ).as_json()))
            })
        except:
            pass
        try:
            chartData.append({
                'Title':'Ethereum', 
                'Data': 
                    list(reversed(td.time_series(
                        symbol="ETH/USD",
                        interval="5min",
                        outputsize=78
                    ).as_json()))
            })
        except:
            pass
        try:
            chartData.append({
                'Title':'Solana', 
                'Data': 
                    list(reversed(td.time_series(
                        symbol="SOL/USD",
                        interval="5min",
                        outputsize=78
                    ).as_json()))
            })
        except:
            pass
        '''
        chartData = [
            {'Title':'Bitcoin', 'Data': btc,  'Fill': '#04ff00' if btc[0]['close'] < btc[-1]['close']   else '#ff0008'},
            {'Title':'Ethereum', 'Data': eth,  'Fill': '#04ff00' if eth[0]['close'] < eth[-1]['close']   else '#ff0008'},
            {'Title':'Solana', 'Data': sol, 'Fill': '#04ff00' if sol[0]['close'] < sol[-1]['close'] else '#ff0008'}
        ]
        '''
    for dataset in chartData:
        if dataset['Data'][0]['close'] < dataset['Data'][-1]['close']:
            dataset['Fill'] = '#04ff00'
        else:
            dataset['Fill'] = '#ff0008'
        for each in dataset['Data']:
            each['datetime'] = datetime.strptime(each['datetime'], '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
            for op in options:
                each[op] = "{:.2f}".format(float(each[op]))
    retDat['news'] = newsData
    retDat['data'] = chartData
    return retDat