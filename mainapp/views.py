from django.shortcuts import render
from django.http.response import HttpResponse
from threading import *
import yfinance as yf
import investpy as inv
from .forms import EmailForm
from .models import Email
from django.core.mail import send_mail

def clear_database(request):
    Email.objects.all().delete()
    return HttpResponse('Banco de dados limpo.')

def stockPicker(request):
    stock_picker = inv.stocks.get_stocks(country='brazil')
    clear_database(request)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            Email.objects.create(address=email)
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
    
    return render(request,'mainapp/stocktracker.html', {'data': data})

def update(request):
    stock = request.GET.get('Key')
    atual_value = request.GET.get('Price')
    atual_stock = yf.Ticker(stock)

    try:
        historical_prices = atual_stock.history(period='1d', interval='1m')
        latest_price = historical_prices['Close'].iloc[-1]
       
    except:
        return HttpResponse(f"Not found data from {stock}")
    
    last_email = Email.objects.last()
    if latest_price > float(atual_value)*1.4:
        send_mail(
            'Preço Alerta: Venda suas ações',
            f'O preço subiu para {latest_price}, que é mais do que 40% acima do valor atual {atual_value}.',
            'seu_email@gmail.com',
            [last_email.address],
            fail_silently=False,
        )
    elif latest_price < float(atual_value)/1.4:
         send_mail(
            'Preço Alerta: Compre mais ações',
            f'O preço caiu para {latest_price}, que é mais do que 40% abaixo do valor atual {atual_value}.',
            'seu_email@gmail.com',
            [last_email.address],
            fail_silently=False,
        )
    
    
    return HttpResponse(latest_price)



