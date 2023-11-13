from flask import Flask
from datetime import datetime
from flask_cors import CORS
import requests as rq
import pandas as pd
import os
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():  
    return 'Hello World!'

@app.route('/query/<string:ticker>/<string:interval>')
def query(ticker, interval):
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
    special = os.getenv('KEY')
    url = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval={intDict[interval]}&outputsize={outDict[interval]}'
    header={'Authorization':f"apikey {special}"}
    response = rq.get(url, headers=header)
    results = response.json()['values']
    results.reverse()
    print(len(results))
    for each in results:
        each['datetime'] = datetime.strptime(each['datetime'], resDict[interval]).strftime(formDict[interval])
        for op in options:
            each[op] = "{:.2f}".format(float(each[op]))
    return results