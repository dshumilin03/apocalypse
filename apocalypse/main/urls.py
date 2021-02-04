from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('statistics', views.statistics),
    path('log-in', views.login),
    path('sign-in', views.signIn),
    path('profile', views.myprofile),
    path('log-out', views.log_out),
]
