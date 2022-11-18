from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="homepage"),
    path("create_event", views.create_event),
    path("event", views.event_detail),
    path("event_success", views.success_page),
    path("register_user", views.register_page),
    path("profile/<username>", views.profile, name='profile'),
    path("browse_events", views.browse_events),
    path("events/<int:id1>/", views.view_event),
    path("bookmark_event/", views.bookmark_event),
    path("register", views.register, name="register"),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
]
