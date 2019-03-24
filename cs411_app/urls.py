from django.urls import path

from . import views

urlpatterns = [
    path('cs411_app/', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('insert_record/', views.insert_record, name='insert_record'),
]
