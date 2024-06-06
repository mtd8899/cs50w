from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("login/", views.login, name="login"),
    path("logoff/", views.logoff, name="logoff"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.random, name="random"),
]