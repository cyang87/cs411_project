from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core import serializers

from django.db import connection

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')
    #return HttpResponse("CS 411 Project: Development Environment Setup")


@csrf_exempt
def insert_record(request):
    print(request.POST)

    user_id = str(request.POST["user_id"])
    user_name = str(request.POST["user_name"])
    gender = str(request.POST["gender"])
    age = int(request.POST["age"])
    state = str(request.POST["state"])
    disease1 = str(request.POST.get("disease1", ""))
    disease2 = str(request.POST.get("disease2", ""))
    disease3 = str(request.POST.get("disease3", ""))
    to_add = []
    if disease1 != "":
        to_add.append(disease1)
    if disease2 != "":
        to_add.append(disease2)
    if disease3 != "":
        to_add.append(disease3)
    if len(to_add) == 0:
        family_disease_history = "NULL"
    else:
        family_disease_history = ",".join(to_add)

    insert_query = "INSERT INTO user_profile (user_id, user_name, gender, age, state, family_disease_history) " + \
                   "VALUES (%s, %s, %s, %s, %s, %s)"

    print(insert_query % (user_id, user_name, gender, age, state, family_disease_history))

    cursor = connection.cursor()
    cursor.execute(insert_query, [user_id, user_name, gender, age, state, family_disease_history])
    result = cursor.fetchall()

    query2 = "SELECT * from user_profile"
    cursor = connection.cursor()
    cursor.execute(query2)
    result = cursor.fetchall()
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]
    print("result")
    print(result)

    return render(request, 'result.html', {'result': result})


@csrf_exempt
def query_databases(request):
    print(request.POST)

    state_filter = str(request.POST["state"])

    query1 = "SELECT State, Y1999 from pop where STATE = %s"

    query2 = "SELECT causes1.CAUSE_NAME, causes1.STATE, causes1.deaths " + \
            "FROM causes as causes1, (SELECT STATE, max(Deaths) as max_deaths " + \
            "FROM causes  WHERE STATE = %s " + \
            "and C113_CAUSE_NAME!='All Causes' GROUP BY STATE) causes2 " + \
            "WHERE causes1.STATE = causes2.STATE and causes2.max_deaths = causes1.DEATHS;"

    cursor = connection.cursor()
    cursor.execute(query2, [state_filter])
    result = cursor.fetchall()

    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]

    print(cursor._last_executed)
    print(result)

@csrf_exempt
def search_record(request):
    print("search")
    print(request.POST)
    user_id = str(request.POST["user_id"])
    query1 = "SELECT user_name, user_id, age, gender, state, family_disease_history from user_profile where user_id = %s"
    cursor = connection.cursor()
    cursor.execute(query1, [user_id])
    result = cursor.fetchall()
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]
    print("result")
    print(result)
    if len(result) == 0:
        return show_results(request, 'No such record found.')
    else:
        return render(request, 'update_info.html', {'result': result})

@csrf_exempt
def updated_page(request):
    user_id = str(request.GET.get("user_id"))
    user_name = str(request.POST["name"])
    state = str(request.POST["state"])
    age = int(request.POST["age"])

    query1 = "UPDATE user_profile SET user_name = %s, state = %s, age = %s WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(query1, [user_name, state, age, user_id])
    query2 = "SELECT * from user_profile"
    cursor = connection.cursor()
    cursor.execute(query2)
    result = cursor.fetchall()
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]
    print("result")
    print(result)
    return render(request, 'result.html', {'result': result})

@csrf_exempt
def deleted_page(request):
    print("delete")
    print(request.GET)
    user_id = str(request.GET.get("user_id"))
    query1 = "DELETE FROM user_profile WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(query1, [user_id])
    return show_results(request)

@csrf_exempt
def show_results(request, message=None):
    query2 = "SELECT * from user_profile"
    cursor = connection.cursor()
    cursor.execute(query2)
    result = cursor.fetchall()
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]
    print("result")
    print(result)
    return render(request, 'result.html', {'result': result, 'message': message})

@csrf_exempt
def analyze(request):
    user_state = str(request.GET.get("state"))
    query1 = "SELECT causes1.CAUSE_NAME, causes1.STATE, causes1.deaths FROM causes as causes1, (SELECT STATE, max(Deaths) as max_deaths FROM causes  WHERE STATE = %s and C113_CAUSE_NAME!='All Causes' GROUP BY STATE) causes2 WHERE causes1.STATE = causes2.STATE and causes2.max_deaths = causes1.DEATHS;"
    cursor = connection.cursor()
    cursor.execute(query1, [user_state])
    result = cursor.fetchall()
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]
    print("result")
    print(result)
    return render(request, 'result.html', {'result': result})

