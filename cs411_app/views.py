from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')
    #return HttpResponse("CS 411 Project: Development Environment Setup")

def test(request):
    return render(request, 'test.html')

@csrf_protect
def insert_record(request):
    print("insert_record")
    print(request.GET["input_test"])



    return render(request, 'test.html')
