from datetime import datetime
import pytz
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from bikingapp import models
from typing import Protocol
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage


from .forms import EventForm, UserRegistrationForm, UserLoginForm, UserUpdateForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect("")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="register.html",
        context={"form": form}
        )

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("")

@user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        public_key = settings.RECAPTCHA_PUBLIC_KEY
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error) 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="login.html",
        context={"form": form}
        )

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
    return render(request, "account/profile.html")


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
