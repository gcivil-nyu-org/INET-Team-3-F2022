from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
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
    path("bookmark_event/", views.bookmark_event),
    path("register_user", views.register_page),
    path("accounts/profile/", views.profile),
    # path("add_friends"      , views.view_friends),
    path("remove_friend/", views.remove_friend),
    path("map", views.display_map),
]
