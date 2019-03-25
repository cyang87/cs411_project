from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core import serializers

from django.db import connection


# Create your views here.

from django.http import HttpResponse

from cs411_app.models import Pop


def index(request):
    return render(request, 'index.html')
    #return HttpResponse("CS 411 Project: Development Environment Setup")


@csrf_exempt
def insert_record(request):
    state_filter = str(request.POST["state"])

    query = "SELECT State, Y1999 FROM pop WHERE State=%s"

    cursor = connection.cursor()
    cursor.execute(query, [state_filter])
    result = cursor.fetchall()

    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]

    print(result)

    return render(request, 'result.html', {'result': result})
