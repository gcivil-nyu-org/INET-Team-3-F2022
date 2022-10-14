from django.http import HttpResponse
from django.shortcuts import render
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

def event_detail(request):

    if request.method == "POST":
        form = EventForm(request.POST)
        #print("Is it valid?")
        if form.is_valid():
            form.save()


    form = EventForm()
    return render(request, 'form.html',{'form':form})