from django.urls import path

from . import views

urlpatterns = [
    path('cs411_app/', views.index, name='index'),
    path('insert_record/', views.insert_record, name='insert_record'),
    path('query_databases/', views.query_databases, name='query_databases'),
    path('search_record/', views.search_record, name='search_record'),
    path('updated_page/', views.updated_page, name='updated_page'),
    path('deleted_page/', views.deleted_page, name='deleted_page'),

]
