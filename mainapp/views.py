from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from threading import *
import yfinance as yf
from django.urls import reverse
import investpy as inv

# Create your views here.
def stockPicker(request):
    stock_picker = inv.stocks.get_stocks(country='brazil')
    
    return render(request,'mainapp/stockpicker.html', {"stockpicker": stock_picker['symbol']})

def stockTracker(request):
    stockpicker = request.GET.getlist('stockpicker')
    
    data = {}
    available_stocks = []

    for i in stockpicker:
        available_stocks.append(i+'.SA')

    for i in available_stocks:
        stock = yf.Ticker(i)

        try:
            historical_prices = stock.history(period='1d', interval='1m')
            latest_price = historical_prices['Close'].iloc[-1]
        except:
            return HttpResponse(f"Not found data from {i}")
        
        
        data.update({i: latest_price})
    print(data)
    return render(request,'mainapp/stocktracker.html', {'data': data})

def update(request):
    stock = request.GET.get('Key')
    atual_stock = yf.Ticker(stock)

    try:
        historical_prices = atual_stock.history(period='1d', interval='1m')
        latest_price = historical_prices['Close'].iloc[-1]
    except:
        return HttpResponse(f"Not found data from {stock}")
    
    return HttpResponse(latest_price)