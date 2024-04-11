from django.shortcuts import render
from django.http import HttpResponse

def initial(request):
    return HttpResponse("Hello World from avs")