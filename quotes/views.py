from django.shortcuts import redirect, render
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
    import requests 
    import json
    # API key: Y3VQ275N******
    # IEX token : pk_d825d7bf2a2744b0b40d188********
    # https://cloud-sse.iexapis.com/stable/stocksUS\?symbols\=spy\&token\=YOUR_TOKEN
    # use this to search symbol api https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tcs&apikey=Y3VQ275N******

    # comapny overiew api https://www.alphavantage.co/query?function=OVERVIEW&symbol=TCS&apikey=Y3VQ275N******
    # endpoint api https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=RELIANCE.BSE&apikey=Y3VQ275N******
    # https://www.alphavantage.co/query?function=OVERVIEW&symbol=aapl&apikey=Y3VQ275NOAGTDO50
    # quote endoint: https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=aapl&apikey=Y3VQ275N******

    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://www.alphavantage.co/query?function=OVERVIEW&symbol=" + ticker +"&apikey=demo")
        try:
            api = json.loads(api_request.content)

        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})
    else:
        
        return render(request, 'home.html', {'ticker': "Enter a ticker symbol above..."})

    

    

    #return render(request, 'home.html', {'api': api})

def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    import requests 
    import json
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added!"))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://www.alphavantage.co/query?function=OVERVIEW&symbol=" + str(ticker_item) +"&apikey=Y3VQ275NOAGTDO50")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."
        
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been Deleted!"))
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})
