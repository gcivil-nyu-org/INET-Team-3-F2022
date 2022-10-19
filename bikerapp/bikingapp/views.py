from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from bikingapp import models
from .forms import EventForm

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

def event_detail(request):

    if request.method == "POST":
        form = EventForm(request.POST)
        print("Is it valid?")
        if form.is_valid():
            form.save()
            return redirect(success_page)
        else:   
            print("Invalid Form")


    form = EventForm()
    return render(request, 'form.html',{'form':form})

def create(request):

    if request.method == "POST":
        form = EventForm(request.POST)
        print("Is it valid?")
        if form.is_valid():
            form.save()
            return redirect(success_page)
        else:   
            print("Invalid Form")

def success_page(request):
    
    location1 = request.POST.get('location')
    created_by = request.POST.get('created_by')
    date_time = request.POST.get('date_time')
    date_created = request.POST.get('date_created')

    obj = models.Event.objects.order_by('id').latest('id')
    print(obj.location)
    context= {'obj1' : obj}
  
    return render(request, 'event_success.html', context)
def Signup(request):
    return render(request, 'account/signup.html')

