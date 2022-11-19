from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="homepage"),
    path("log_workout", views.log_workout),
    path("log_workout/post_workout", views.post_workout),
    path("log_workout/post_workout/success", views.workout_success),
    path("workout_history", views.workout_history),
    path("workout_history/<int:id1>/", views.view_workout),
    path("create_event", views.create_event),
    path("create_event/post_event", views.post_event),
    path("create_event/post_event/success", views.event_success),
    path("browse_events", views.browse_events),
    path("browse_events/<int:id1>/", views.view_event),
    # path("events/<int:id1>/", views.view_event),
    path("bookmark_event/", views.bookmark_event),
    path("profile/<username>", views.profile, name='profile'),
    path("register", views.register, name="register"),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    # path("add_friends", views.view_friends),
    path("remove_friend/", views.remove_friend),
    path("map", views.display_map),
]
