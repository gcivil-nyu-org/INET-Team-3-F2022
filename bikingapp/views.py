from datetime import datetime
import pytz
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from bikingapp import models
from .forms import EventForm, FriendMgmtForm, WorkoutForm
from django.http import HttpResponseRedirect

"""
, SnippetForm
"""

# def index(request):
#    return HttpResponse("Hello, world. You're at the Biking App index.")
"""
def contact(request):

    if request.method == "POST":
        form = EventForm(request.POST)
        #print("Is it valid?")
        if form.is_valid():
            location = form.cleaned_data['location']
            date_time = form.cleaned_data['date_time']
            public_private = form.cleaned_data['public_private']
            description = form.cleaned_data['description']

            print(location, date_time, public_private, description)


    form = EventForm()
    return render(request, 'form.html',{'form':form})
"""


def home(request):
    return render(request, "base.html")


@login_required
def log_workout(request):
    """
    Prompt user with log workout form
    """
    tz_NY = pytz.timezone("America/New_York")
    form = WorkoutForm(
        {
            "created_by": request.user,
            "date": datetime.now(tz_NY),
            "date_created": datetime.now(tz_NY),
            "time": datetime.now(tz_NY).time(),
        }
    )
    return render(request, "workout/log_workout.html", {"form": form})


@login_required
def post_workout(request):
    """
    Attempt POST request after user submits form
    """
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(workout_success)
        else:
            print("Invalid Form")


@login_required
def workout_success(request):
    """
    If form is valid, display workout success page
    """
    obj = models.Event.objects.order_by("id").latest("id")
    context = {"obj1": obj}

    return render(request, "workout/workout_success.html", context)


@login_required
def workout_history(request):
    """
    display workouts created by that user in sequential order
    """
    obj = models.Workout.objects.filter(created_by=request.user).order_by("id")
    context = {"obj1": obj}
    return render(request, "workout/workout_history.html", context)


def view_workout(request, id1):
    """
    query db with id open workout page
    """
    obj = models.Workout.objects.filter(id=id1).order_by("id")
    context = {"obj1": obj}
    return render(request, "workout/view_workout.html", context)


@login_required
def create_event(request):
    """
    display form
    """
    tz_NY = pytz.timezone("America/New_York")
    form = EventForm(
        {
            "created_by": request.user,
            "state": "New York",
            "date": datetime.now(tz_NY),
            "date_created": datetime.now(tz_NY),
            "time": datetime.now(tz_NY).time(),
        }
    )
    return render(request, "event/event_info.html", {"form": form})


@login_required
def post_event(request):
    """
    attempt POST Request after submitting EventForm
    """
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(event_success)
        else:
            print("Invalid Form")


def event_success(request):
    """
    call success page if form successful
    """
    obj = models.Event.objects.order_by("id").latest("id")
    context = {"obj1": obj}

    return render(request, "event/event_success.html", context)


def browse_events(request):
    obj_private = models.Event.objects.order_by("id").filter(event_type="private")
    obj_public = models.Event.objects.order_by("id").filter(event_type="public")
    if request.user.is_anonymous:
        context = {"obj1": obj_private, "obj2": obj_public}
    else:
        bookmarked_events = models.BookmarkEvent.objects.filter(
            user=request.user
        ).values_list("event", flat=True)
        context = {
            "obj1": obj_private,
            "obj2": obj_public,
            "bookmarked_events": bookmarked_events,
        }
    return render(request, "event/browse_events.html", context)


def view_event(request, id1):
    obj = models.Event.objects.order_by("id").filter(id=id1)
    context = {"obj1": obj}
    return render(request, "event/view_event.html", context)


def bookmark_event(request):
    data = json.loads(request.body)
    eventId = data["eventId"]
    action = data["action"]
    user = request.user
    event = models.Event.objects.get(id=eventId)
    bookmarkItem, created = models.BookmarkEvent.objects.get_or_create(
        user=user, event=event
    )
    if action == "unbookmark":
        bookmarkItem.delete()
    return JsonResponse("Event was bookmarked", safe=False)


def register_page(request):
    return render(request, "account/signup.html")


@login_required
def profile(request):
    # adding friends code
    obj = models.FriendMgmt.objects.get_or_create(
        user=request.user, friend=request.user
    )
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = FriendMgmtForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            friend_username = form.cleaned_data["friend_username"]
            if models.User.objects.filter(username=friend_username).first() is not None:
                obj = models.FriendMgmt(
                    user=request.user,
                    friend=models.User.objects.filter(username=friend_username).first(),
                )
                if not models.FriendMgmt.objects.filter(
                    user=request.user,
                    friend=models.User.objects.filter(username=friend_username).first(),
                ).exists():
                    obj.save()

            return HttpResponseRedirect("/accounts/profile/")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = FriendMgmtForm()
    friends1 = models.FriendMgmt.objects.filter(user=request.user)
    return render(
        request,
        "account/profile.html",
        {"friends": {"form": form, "friends_list": friends1}},
    )
    # return render(request, "account/profile.html")


# @login_required
# def view_friends(request):
#     obj = models.FriendMgmt.objects.get_or_create(
#         user=request.user, friend=request.user
#     )
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         form = FriendMgmtForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             friend_username = form.cleaned_data["friend_username"]
#             if models.User.objects.filter(username=friend_username).first() is not None: # noqa: E501
#                 obj = models.FriendMgmt(
#                     user=request.user,
#                     friend=models.User.objects.filter(username=friend_username).first(), # noqa: E501
#                 )
#                 if not models.FriendMgmt.objects.filter(
#                     user=request.user,
#                     friend=models.User.objects.filter(username=friend_username).first(), # noqa: E501
#                 ).exists():
#                     obj.save()

#             return HttpResponseRedirect("/add_friends")
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = FriendMgmtForm()
#     friends1 = models.FriendMgmt.objects.filter(user=request.user)
#     return render(request, "friends.html", {"form": form, "friends_list": friends1}) # noqa: E501
#     # return {"requests":request, "friends":{"form": form, "friends_list": friends1}} # noqa: E501


def display_map(request):
    return render(request, "map.html")
