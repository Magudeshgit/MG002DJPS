from django.shortcuts import render,redirect
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
    model_bills = bill.objects.all()
    ic_stock  = 0
    for i in model:
        if i.quantity < i.maximumstock:
            ic_stock+=1

    

    context = {
        'overviewdata':model.reverse()[:5],
        'stockcount': model.count(),
        'iccount': ic_stock,
        'billcount': model_bills.count(),
        }
    
    return render(request, "core/dashboard.html", context)   

def stocks(request):
    stocks = stock.objects.all()
    return render(request, "core/stocks.html", {'stocks':stocks})

def incomingstocks(request):
    stocks = stock.objects.all()
    return render(request, "core/incomingstocks.html", {'stocks':stocks})

def damagedmaterials(request):
    return render(request, "core/damagedmaterials.html")

def addstock(request):
    return render(request, "core/addstock.html")

def bills(request):
    _bill = reversed(bill.objects.all())
    print(_bill)
    
    context = {'bills':_bill}
    return render(request, "core/bills.html", context)

def newbill(request):
    if request.method == 'POST':
        print(request.POST)
        customer = request.POST.get('customer')
        items = request.POST.get('items')
        billstatus = request.POST.get('billstatus')
        subtotal = request.POST.get('subtotal')
        discount = request.POST.get('discount')
        grandtotal = request.POST.get('grandtotal')

        items = json.loads(items)
        jsondata = {'items': items, 'subtotal': subtotal, 'discount': discount, 'grandtotal': grandtotal}
        jsondata = json.dumps(jsondata)

        print('data',items)
        if billstatus == 'false':
            for i in items:
                _product = stock.objects.get(productname=i[0])
                _product.quantity = _product.quantity - int(i[1])
                _product.save()

        _customer = client.objects.get(clientname=customer)
        new_bill = bill.objects.create(products=jsondata, grandtotal=int(grandtotal))   
        new_bill.client.add(_customer)
        new_bill.save()
    
    clients = client.objects.values_list('clientname')
    stocks = stock.objects.values_list('productname')
    clients = json.dumps(list(clients.values()))
    stocks = json.dumps(list(stocks.values()))
    
    context = {"clients": clients, "products": stocks}
    return render(request, "core/newbill.html", context)

def reviewbill(request,pk=None):
    if request.method == 'POST':
        print(request.POST)
        customer = request.POST.get('customer')
        items = request.POST.get('items')
        billstatus = request.POST.get('billstatus')
        subtotal = request.POST.get('subtotal')
        discount = request.POST.get('discount')
        grandtotal = request.POST.get('grandtotal')

        items = json.loads(items)
        jsondata = {'items': items, 'subtotal': subtotal, 'discount': discount, 'grandtotal': grandtotal}
        jsondata = json.dumps(jsondata)

        # Handling Central Stock
        if billstatus == 'false':
            for i in items:
                _product = stock.objects.get(productname=i[0])
                _product.quantity = _product.quantity - int(i[1])
                _product.save()
        else:
            for i in items:
                _product = stock.objects.get(productname=i[0])
                _product.quantity = _product.quantity + int(i[1])
                _product.save()

        _customer = client.objects.get(clientname=customer)
        obj = bill.objects.get(id=pk)
        obj.products=jsondata
        obj.grandtotal=int(grandtotal)
        obj.client.add(_customer)
        obj.save()
        return redirect('/bills')

    clients = client.objects.values_list('clientname')
    stocks = stock.objects.values_list('productname')
    clients = json.dumps(list(clients.values()))
    stocks = json.dumps(list(stocks.values()))

    _editbill = bill.objects.get(id=pk)
    context = {'bill': _editbill, 'customer': _editbill.client.all()[0].clientname, 'items': _editbill.products, "clients": clients, "products": stocks}
    return render(request, "core/editbill.html", context)

def clientbook(request):
    clients = client.objects.all()
    return render(request, "core/clientbook.html", {'clients': clients})

def laborbook(request):
    labors = labor.objects.all()
    return render(request, "core/laborbook.html", {'labors': labors})