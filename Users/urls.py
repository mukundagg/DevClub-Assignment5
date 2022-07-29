from django.contrib import admin
from django.urls import path, include
from . import views as user_views

urlpatterns = [
    path("register/", user_views.register),
    path("register/create/", user_views.make),
    path("login/", user_views.login),
    path("login/auth/", user_views.check),
    path("logout/", user_views.logout),
    path("createcourse/", user_views.makecourse),
    path("<slug:entryNo>", user_views.load_profile),
    path("editprofile/", user_views.edit_profile)
]