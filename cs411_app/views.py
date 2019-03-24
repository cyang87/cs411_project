from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    print(request)
    return render(request, 'index.html')
    #return HttpResponse("CS 411 Project: Development Environment Setup")

def test(request):
    return render(request, 'test.html')
