from . import views, templates
from django.contrib import admin
from django.urls import path, include

app_name = "prac"

urlpatterns = [
    path('', views.index, name='index'),
    path('print', views.print_excel, name='print_excel'),
    path('printCsv', views.print_csv, name='print_csv'),
]
