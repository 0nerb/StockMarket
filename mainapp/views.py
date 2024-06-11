from django.shortcuts import render
from django.http.response import HttpResponse
from threading import *
import queue
import yfinance as yf
import pandas as pd
import investpy as inv

# Create your views here.
def stockPicker(request):
    stock_picker = inv.stocks.get_stocks(country='brazil')
    
    return render(request,'mainapp/stockpicker.html', {"stockpicker": stock_picker['symbol']})

def stockTracker(request):
    stockpicker = request.GET.getlist('stockpicker')
    
    data = {}
    all_stocks = inv.stocks.get_stocks(country='brazil')
    available_stocks = []

    for i in stockpicker:
        available_stocks.append(i+'.SA')
        
    '''for i in stockpicker:
        print(i)
        if i in available_stocks:
            pass
        else:
            return HttpResponse("ERROR")'''
        
    for i in available_stocks:
        stock = yf.Ticker(i)

        try:
            historical_prices = stock.history(period='1d', interval='1m')
            latest_price = historical_prices['Close'].iloc[-1]
        except:
            return HttpResponse("possibly delisted; No price data found")
        
        
        data.update({i: latest_price})
    print(data)
    return render(request,'mainapp/stocktracker.html', {'data': data})