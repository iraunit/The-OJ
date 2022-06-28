from django.urls import path,include
from django.shortcuts import redirect
from .import views


urlpatterns = [
    path('',views.home),
    path("login",views.login_page),
    path("register",views.register),
    path("logout",views.logoutUser)
    
]
