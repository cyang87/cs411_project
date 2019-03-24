from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from cs411_app.models import Easy

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

    p = Easy(request.GET["input_test"])
    p.save()

    return render(request, 'test.html')
