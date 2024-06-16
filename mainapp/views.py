from django.shortcuts import render
from django.http.response import HttpResponse
from threading import *
import yfinance as yf
import investpy as inv
from .forms import EmailForm
from .models import Email

# Create your views here.
def stockPicker(request):
    stock_picker = inv.stocks.get_stocks(country='brazil')
    # Initialize the form
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            Email.objects.create(address=email)
            return HttpResponse('Thank you for submitting your email!')
    else:
        form = EmailForm()
    
    return render(request,'mainapp/stockpicker.html', {"stockpicker": stock_picker['symbol'], 'form': form})

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
            atual = historical_prices.iloc[-1]

        except:
            return HttpResponse(f"Not found data from {i}")
        
        
        data.update({i: atual})
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



