from django.urls import path

from . import views

# Giving it an app name caused me to get a lot of errors, "NoReverseMatch at /"
# app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    # Adding http://localhost:8000/wiki as path for wiki/TITLE requirement
    path("wiki/<str:TITLE>", views.wiki, name="wiki"),
    # Route guest to http://localhost:8000/new_page.html
    path("new_page.html", views.new_page, name="new_page"),
    # Adding http://locahost:8000/random as path, redirects to wiki/TITLE
    path("random", views.random, name="random"),
    # Adding http://localhost:8000/edit_page/TITLE as path, redirects
    # to other routes in this file will not work, unless you go back one directory
    # e.g root folder http://localhost:8000/
    path("edit_page/<str:TITLE>", views.edit_page, name="edit_page")
]
