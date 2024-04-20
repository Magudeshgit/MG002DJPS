from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def home(request):
    return HttpResponse("Home page")
@login_required(login_url='/auth/signup/')
def dashboard(request):
    return render(request, "core/dashboard.html")   

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
    return render(request, "core/newbill.html")

def clientbook(request):
    return render(request, "core/clientbook.html")