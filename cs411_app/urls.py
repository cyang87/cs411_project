from django.urls import path

from . import views

urlpatterns = [
    path('cs411_app/', views.index, name='index'),
    path('insert_record/', views.insert_record, name='insert_record'),
    path('search_record/', views.search_record, name='search_record'),
]
