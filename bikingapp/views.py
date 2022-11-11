from datetime import datetime
import pytz
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from bikingapp import models
from .models import Event
from .forms import EventForm,CommentForm
from django.shortcuts import render, get_object_or_404

'''
, SnippetForm
'''

#def index(request):
#    return HttpResponse("Hello, world. You're at the Biking App index.")
'''
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
'''
def home(request):
    return render(request, 'base.html')

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
    #form = EventForm({'created_by':request.user})
    #form = EventForm()     
    tz_NY = pytz.timezone('America/New_York') 
    form = EventForm({'created_by':request.user,'state':'New York','date':datetime.now(tz_NY),'date_created':datetime.now(tz_NY), 'time':datetime.now(tz_NY).time()})
    return render(request, 'form.html',{'form':form})

@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        print("form",form)
        print("Is it valid?")
        if form.is_valid():
            form.save(commit=True)
            print("form 2 saved")
            return redirect(success_page)
        else:   
            print("Invalid Form")

def success_page(request):
    
    #location1 = request.POST.get('location')
    #created_by = request.POST.get('created_by')
    #date_time = request.POST.get('date')
    #date_time = request.POST.get('time')
    #date_created = request.POST.get('date_created')

    obj = models.Event.objects.order_by('id').latest('id')
    print(obj.title)
    context= {'obj1' : obj}
  
    return render(request, 'event_success.html', context)

def register_page(request):
    return render(request,'account/signup.html')

@login_required
def profile(request):
    return render(request, 'account/profile.html')
    
def browse_events(request):  
    obj_private = models.Event.objects.order_by('id').filter(event_type='private')
    obj_public = models.Event.objects.order_by('id').filter(event_type='public')
    print("user",request.user)
    if request.user.is_anonymous:
        context= {'obj1' : obj_private, 'obj2' : obj_public}
    else:
        bookmarked_events = models.BookmarkEvent.objects.filter(user= request.user).values_list("event",flat = True)
        context= {'obj1' : obj_private, 'obj2' : obj_public,'bookmarked_events':bookmarked_events}
    print("outside if")
    return render(request, 'browse_events.html', context)

def view_event(request, id1):
    obj= models.Event.objects.order_by('id').filter(id=id1)
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
    context= {'obj1' : obj,"post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,}
    return render(request, 'view_event.html', context)

def bookmark_event(request):
    print(request.body)
    data = json.loads(request.body)
    eventId = data["eventId"]
    action = data["action"]
    print("eventId",eventId)
    print("action", action)
    user = request.user
    event = models.Event.objects.get(id=eventId)
    bookmarkItem, created = models.BookmarkEvent.objects.get_or_create(user = user, event = event)
    if action == "unbookmark":
        bookmarkItem.delete()
    return JsonResponse('Event was bookmarked',safe=False)