from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("addPage", views.add_page, name="addPage"),
    path("random", views.random, name="random"),
    path("<str:title>", views.entry_page, name="entry_page"),
    path("<str:title>/edit", views.edit_page, name="edit_page"),
]
