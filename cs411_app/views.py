from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core import serializers
import collections
from django.db import connection
from .keywords import *

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')
    # return HttpResponse("CS 411 Project: Development Environment Setup")


@csrf_exempt
def insert_record(request):
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

    query2 = "SELECT user_id from user_profile"
    cursor = connection.cursor()
    cursor.execute(query2)
    result = cursor.fetchall()
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]
    keys = [item['user_id'] for item in result]

    if user_id in keys:
        print(cursor._last_executed)
        return show_results(request, "Did not insert, user_id already exists.")

    else:

        insert_query = "INSERT INTO user_profile (user_id, user_name, gender, age, state, family_disease_history) " + \
                       "VALUES (%s, %s, %s, %s, %s, %s)"

        cursor = connection.cursor()
        cursor.execute(insert_query, [user_id, user_name, gender, age, state, family_disease_history])
        result = cursor.fetchall()
        print(cursor._last_executed)

        return show_results(request)


@csrf_exempt
def search_record(request):
    user_id = str(request.POST["user_id"])
    query1 = "SELECT user_name, user_id, age, gender, state, family_disease_history from user_profile where user_id = %s"
    cursor = connection.cursor()
    cursor.execute(query1, [user_id])
    result = cursor.fetchall()
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]
    print(cursor._last_executed)

    print(result)
    if len(result) == 0:
        return show_results(request, 'No such record found.')
    else:
        return render(request, 'update_info.html', {'result': result})


@csrf_exempt
def updated_page(request):
    user_id = str(request.POST.get("user_id"))
    user_name = str(request.POST["name"])
    state = str(request.POST["state"])
    age = int(request.POST["age"])

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

    query1 = "UPDATE user_profile SET user_name = %s, state = %s, age = %s, family_disease_history = %s WHERE user_id = %s"
    cursor = connection.cursor()

    cursor.execute(query1, [user_name, state, age, family_disease_history, user_id])
    print(cursor._last_executed)

    return show_results(request)


@csrf_exempt
def deleted_page(request):
    user_id = str(request.POST.get("user_id"))
    query1 = "DELETE FROM user_profile WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(query1, [user_id])

    print(cursor._last_executed)

    return show_results(request)


@csrf_exempt
def show_results(request, message=None):
    query2 = "SELECT * from user_profile"
    cursor = connection.cursor()
    cursor.execute(query2)
    result = cursor.fetchall()
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]
    return render(request, 'result.html', {'result': result, 'message': message})


@csrf_exempt
def analyze(request):
    user_id = str(request.POST["user_id"])

    query_num = int(request.POST.get('query_num', -1))

    query_sym = "SELECT Name FROM symptoms"
    cursor = connection.cursor()
    cursor.execute(query_sym)
    result = cursor.fetchall()
    columns = cursor.description

    sym_vocab = []
    for r in result:
        sym_vocab.append(r[0])

    if query_num != -1:
        if query_num == 1:

            query1 = "SELECT * FROM user_profile WHERE user_id = %s"
            cursor = connection.cursor()
            cursor.execute(query1, [user_id])
            result = cursor.fetchall()
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]

            user_state = result[0]['state']
            year = int(request.POST.get('leadyear', -1))

            if year != -1:

                query1 = "SELECT causes1.CAUSE_NAME, causes1.STATE, causes1.deaths, causes1.YEAR FROM causes as causes1, " + \
                         "(SELECT STATE, max(Deaths) as max_deaths FROM causes  WHERE STATE = %s and YEAR = %s " + \
                         "and C113_CAUSE_NAME!='All Causes' GROUP BY STATE) causes2 WHERE causes1.STATE = causes2.STATE " + \
                         "and causes2.max_deaths = causes1.DEATHS;"
                cursor = connection.cursor()
                cursor.execute(query1, [user_state, year])
                result = cursor.fetchall()
                columns = cursor.description
                print(cursor._last_executed)

                result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]
            else:
                result = []

        elif query_num == 2:

            query1 = "SELECT * FROM user_profile WHERE user_id = %s"
            cursor = connection.cursor()
            cursor.execute(query1, [user_id])
            result = cursor.fetchall()
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]

            user_state = result[0]['state']
            user_age = result[0]['age']
            print(user_age)
            # query1 = "select AADR/100000 from causes where C113_CAUSE_NAME = 'All Causes' and State = %s limit 1"
            # cursor = connection.cursor()
            # cursor.execute(query1, [user_state])
            # result = cursor.fetchall()
            # columns = cursor.description
            # print(cursor._last_executed)
            # print(result[0][0])
            # num1 = result[0][0]

            query2 = "select CAUSE_NAME, Deaths/Y2007 as DR, AADR/100000 as AADR from " + \
                     "(causes natural join pop) where State = %s and YEAR = 2007 and " + \
                     "CAUSE_NAME <> 'All Causes' order by DR desc limit 5";
            cursor = connection.cursor()
            cursor.execute(query2, [user_state])
            result = cursor.fetchall()
            columns = cursor.description
            print(cursor._last_executed)
            print(result)
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]

            for r in result:
                if r['AADR'] < r['DR']:
                    if 25 <= user_age <= 45:
                        r['Likeliness'] = "Less likely for your age"
                    else:
                        r['Likeliness'] = "More likely for your age"

                else:
                    if 25 <= user_age <= 45:
                        r['Likeliness'] = "More likely for your age"
                    else:
                        r['Likeliness'] = "Less likely for your age"

            # if num1<num2:
            #     if user_age>=30 or user_age<=50:
            #         result = "Less likely"
            #     else:
            #         result = "More likely"
            # else:
            #     if user_age>=30 or user_age<=50:
            #         result = "More likely"
            #     else:
            #         result = "Less likely"

        elif query_num == 3:

            query1 = "SELECT State, Y2007 as avg_pop, avg_death FROM(SELECT State, avg(Deaths) as " + \
                     "avg_death FROM causes WHERE C113_CAUSE_NAME= 'All Causes' GROUP BY State)as one " + \
                     " NATURAL JOIN (SELECT State, Y2007 FROM pop) as two"

            cursor = connection.cursor()
            cursor.execute(query1)
            result = cursor.fetchall()
            columns = cursor.description
            print(cursor._last_executed)

            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]

        elif query_num == 4:

            condition = str(request.POST.get("symptoms", ""))

            print(condition)
            keywords = get_keywords(condition, sym_vocab)
            keywords = ['%' + keyword + '%' for keyword in keywords]

            n_result = []
            d_set = set()
            for symptom in keywords:
                each_symp = symptom.split("+")
                query1 = "select t2.Name, t.weight as Likelihood from sym_dis t, symptoms t1, disease t2 " + \
                         "where t2.DiseaseID = t.DiseaseID and t1.SymptomID = t.SymptomID and " + \
                         "LOWER(t1.name) LIKE LOWER(%s) order by t.weight limit 5;"

                cursor = connection.cursor()
                cursor.execute(query1, each_symp)
                result = cursor.fetchall()
                columns = cursor.description

                print(cursor._last_executed)

                t_result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]

                mapper = {1: 'Somewhat likely', 2: 'Likely', 3: 'Very likely'}
                for r in t_result:
                    if r['Name'] in d_set:
                        for n in n_result:
                            if n['Name'] == r['Name']:
                                n['Likelihood'] = max(n['Likelihood'], r['Likelihood'])
                    else:
                        d_set.add(r['Name'])
                        n_result.append(r)

            for r in n_result:
                r['Likelihood'] = mapper[r['Likelihood']]

            result = n_result

        elif query_num == 5:
            print("symptoms")
            symptom1 = str(request.POST.get("symptom1", ""))
            symptom2 = str(request.POST.get("symptom2", ""))
            symptom3 = str(request.POST.get("symptom3", ""))
            symptom4 = str(request.POST.get("symptom4", ""))
            symptom5 = str(request.POST.get("symptom5", ""))
            result = []
            to_add = []
            if symptom1 != "":
                # print(symptom1)
                to_add.append("%" + symptom1 + "%")
            if symptom2 != "":
                # print(symptom2)
                to_add.append("%" + symptom2 + "%")
            if symptom3 != "":
                # print(symptom3)
                to_add.append("%" + symptom3 + "%")
            if symptom4 != "":
                # print(symptom4)
                to_add.append("%" + symptom4 + "%")
            if symptom5 != "":
                # print(symptom5)
                to_add.append("%" + symptom5 + "%")
            n_result = []

            resultfin = dict()
            print(to_add)
            symptoms_dict = collections.defaultdict(int)
            for symptom in to_add:
                # print(symptom)
                
                query1 = "select t2.Name as d_name, t.Weight from sym_dis t, symptoms t1, disease t2 " + \
                    "where t2.DiseaseID = t.DiseaseID and t1.SymptomID = t.SymptomID and t1.name LIKE %s order by t.weight limit 15;"

                cursor = connection.cursor()
                cursor.execute(query1, symptom)
                result = cursor.fetchall()
                columns = cursor.description
                print(cursor._last_executed)
                result = list(result)
                print("res")
                print(result)

                for disease in result:
                    disease_name = disease[0]
                    w = disease[1]
                    query2 = "select t1.name from sym_dis t, symptoms t1, disease t2 " + \
                    "where t2.DiseaseID = t.DiseaseID and t1.SymptomID = t.SymptomID and t2.Name LIKE %s limit 5;"
                    cursor = connection.cursor()
                    cursor.execute(query2, disease_name)
                    result = cursor.fetchall()
                    columns = cursor.description
                    # print(cursor._last_executed)
                    result = list(result)
                    for r in result:
                        symptoms_dict[r[0]] += int(w)
                # print(symptoms_dict)

            cnt = 0
            result2 = dict()
            for key, value in sorted(symptoms_dict.items(), key=lambda item: item[1], reverse = True):
                if cnt == 5:
                    break
                if ("%"+key+"%").lower() not in to_add:
                    cnt += 1
                    result2[key] = value

            for key, val in result2.items():
                if val >= 10:
                    result2[key] = 'Highly correlated'
                else:
                    result2[key] = 'Possibly correlated'

            ans = []
            ans.append(result2)
            result = ans
            print(result)
        else:
            result = []

    else:
        result = []

    return render(request, 'analyze.html', {'result': result, 'user_id': user_id, 'query_num': query_num})
