from datetime import datetime
import pytz
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from bikingapp import models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import EventForm, FriendMgmtForm, WorkoutForm, Account, CommentForm 
from .models import Event
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect


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
    return render(request, "base.html", {"username":request.user})


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
    post = get_object_or_404(Event, id=id1)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        "obj1": obj,
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
    }
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
def current_user_profile(request):
    return redirect('/accounts/profile/'+str(request.user.username), username=request.user.username)

@login_required
def profile(request, username):
    user_page = User.objects.get(username= username)
    user_account = Account.objects.get(user = user_page)
    if request.user.username == username:
        print("equal")
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
            {"friends": {"form": form, "friends_list": friends1},
            "user_page":user_page, "user_account":user_account},
        )
    else:
        return render(request,"account/profile.html",{"user_page":user_page,"user_account":user_account})


def remove_friend(request):
    print(request.body)
    data = json.loads(request.body)
    friend_username = data["friend_username"]
    print("Friend Username:", friend_username)
    user = request.user
    friend = models.User.objects.filter(username=friend_username).first()
    if user != friend:
        print("friend user object", friend)

        friend1 = models.FriendMgmt.objects.get(user=request.user, friend=friend)

        print("Friend management object user", friend1.user)

        friend1.delete()

        return JsonResponse("Friend was deleted", safe=False)
    else:
        return JsonResponse("Friend can't be deleted", safe=False)


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
