from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    path('hello', views.index),
    path('', views.login_action)
]
