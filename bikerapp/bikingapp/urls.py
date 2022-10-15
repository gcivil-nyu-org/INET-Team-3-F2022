from django.urls import path,include
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.home),
    path('create',views.create),
    path('event', views.event_detail),
    path('event_success', views.success_page)
]
