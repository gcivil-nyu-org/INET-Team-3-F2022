from django.urls import path,include
from django.contrib import admin

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    #path('',views.contact),
    path('event', views.event_detail),
    path('event_success', views.success_page)
]
