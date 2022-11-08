from datetime import datetime
import pytz
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from bikingapp import models
from .forms import EventForm, FriendMgmtForm
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
def event_detail(request):
    # if request.method == "POST":
    #     #dct = {'created_by' : request.user}
    #     form = EventForm(request.POST)
    #     print("Is it valid?")
    #     if form.is_valid():
    #         form.save()
    #         print("form 1 saved")
    #         return redirect(success_page)
    #     else:
    #         print("Invalid Form")
    # form = EventForm({'created_by':request.user})
    # form = EventForm()
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
    return render(request, "form.html", {"form": form})


@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        print("form", form)
        print("Is it valid?")
        if form.is_valid():
            form.save(commit=True)
            print("form 2 saved")
            return redirect(success_page)
        else:
            print("Invalid Form")


def success_page(request):

    # location1 = request.POST.get('location')
    # created_by = request.POST.get('created_by')
    # date_time = request.POST.get('date')
    # date_time = request.POST.get('time')
    # date_created = request.POST.get('date_created')

    obj = models.Event.objects.order_by("id").latest("id")
    print(obj.title)
    context = {"obj1": obj}

    return render(request, "event_success.html", context)


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


def browse_events(request):
    obj_private = models.Event.objects.order_by("id").filter(event_type="private")
    obj_public = models.Event.objects.order_by("id").filter(event_type="public")
    print("user", request.user)
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
    print("outside if")
    return render(request, "browse_events.html", context)


def view_event(request, id1):
    obj = models.Event.objects.order_by("id").filter(id=id1)
    context = {"obj1": obj}
    return render(request, "view_event.html", context)


def bookmark_event(request):
    print(request.body)
    data = json.loads(request.body)
    eventId = data["eventId"]
    action = data["action"]
    print("eventId", eventId)
    print("action", action)
    user = request.user
    event = models.Event.objects.get(id=eventId)
    bookmarkItem, created = models.BookmarkEvent.objects.get_or_create(
        user=user, event=event
    )
    if action == "unbookmark":
        bookmarkItem.delete()
    return JsonResponse("Event was bookmarked", safe=False)


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