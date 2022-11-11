from asyncio.subprocess import SubprocessStreamProtocol
from atexit import register
from django.urls import path,include
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.home),
    path('create_event',views.create_event),
    path('event', views.event_detail),
    path('event_success', views.success_page),
    path('register_user', views.register_page),
    path('accounts/profile/', views.profile),
    path('browse_events', views.browse_events),
    path('events/<int:id1>/', views.view_event),
    path('bookmark_event/', views.bookmark_event),
    #path('<slug:slug>/', views.post_detail, name='post_detail')

]
