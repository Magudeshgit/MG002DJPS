from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import stock, client, bill, labor
from django.db.models import Count
import json


def home(request):
    return HttpResponse("Home page")
@login_required(login_url='/auth/signup/')
def dashboard(request):
    model = stock.objects.all().order_by('productname')
    most_retrieved_item = stock.objects.values('productname').annotate(count=Count('productname')).order_by('-count').first()
    print(most_retrieved_item)

    context = {
        'overviewdata':model.reverse()[:5],
        'stockcount': model.count(),
        }
    return render(request, "core/dashboard.html", context)   

def stocks(request):
    return render(request, "core/stocks.html")

def incomingstocks(request):
    return render(request, "core/incomingstocks.html")

def outgoingstocks(request):
    return render(request, "core/outgoingstocks.html")

def damagedmaterials(request):
    return render(request, "core/damagedmaterials.html")

def bills(request):
    return render(request, "core/bills.html")

def newbill(request):
    clients = client.objects.values_list('clientname')
    stocks = stock.objects.values_list('productname')
    
    clients = json.dumps(list(clients.values()))
    stocks = json.dumps(list(stocks.values()))

    context = {"clients": clients, "products": stocks}
    return render(request, "core/newbill.html", context)

def clientbook(request):
    return render(request, "core/clientbook.html")