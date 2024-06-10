from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    import requests
    import json
    # pk_62c9bc84a490436487d7b331047544c9
    # sk_665fe1b755ab4c86b413f4affa24ba91
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=sk_665fe1b755ab4c86b413f4affa24ba91")
        try:
            #gets data from api and saves it to variable
            api = json.loads(api_request.content)
        except Exception as e:
            #if it fails it will throw an error
            api = "Error..."
        return render(request, 'home.html', {'api':api})
    else:
        return render(request, 'home.html', {'Ticker':"Please Enter a Stock Ticker Sybmol..."})



    #__________________________________________



def about(request):
    #__________________________________________
    context =  {}
    return render(request, 'about.html', context)


def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added!")
            return redirect('add_stock')
        else:
            messages.success(request, ('Edit Invalid: Your Submission was Blank!'))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_id in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_id) + "/quote?token=sk_665fe1b755ab4c86b413f4affa24ba91")
            try:
                #gets data from api and saves it to variable
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                #if it fails it will throw an error
                api = "Error..."
        #__________________________________________
        context =  {'ticker': ticker,'output':output}
        return render(request, 'add_stock.html', context)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})

def delete(request, stock_id):
    #gets the item from the database with the id number from the django database
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ('Stock Has Been Deleted!'))
    return redirect('delete_stock')
