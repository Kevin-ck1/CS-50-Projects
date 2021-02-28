from django.urls import path, re_path
from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("search", views.search, name="search"),
    path("add_entry", views.add_entry, name="add_entry"),
    path("random", views.random, name="random"),
    path("<str:title>", views.entry_page, name="entry_page"),
    path("<str:title>/edit_entry", views.edit_entry, name="edit_entry")
    #['(?P<title>[^/]+)$']
]
