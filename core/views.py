from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def home(request):
    return HttpResponse("Home page")
@login_required(login_url='/auth/signup/')
def initial(request):
    return render(request, "core/index.html")   

