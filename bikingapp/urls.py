from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("create_event", views.create_event),
    path("event", views.event_detail),
    path("event_success", views.success_page),
    path("register_user", views.register_page),
    path("accounts/profile/", views.profile),
    path("browse_events", views.browse_events),
    path("events/<int:id1>/", views.view_event),
    path("bookmark_event/", views.bookmark_event),
    path("register", views.register, name="register"),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
