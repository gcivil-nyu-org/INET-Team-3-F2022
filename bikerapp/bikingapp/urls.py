from asyncio.subprocess import SubprocessStreamProtocol
from atexit import register
from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.home),
    path("create", views.create),
    path("event", views.event_detail),
    path("event_success", views.success_page),
    path("register_user", views.register_page),
    path("accounts/profile/", views.profile),
]
