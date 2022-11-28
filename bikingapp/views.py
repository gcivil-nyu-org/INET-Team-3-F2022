from datetime import datetime
import pytz
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from bikingapp import models
from django.http import HttpResponseRedirect

# from typing import Protocol
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string

# from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from .models import Event, Comment, Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import (
    EventForm,
    UserRegistrationForm,
    UserLoginForm,
    UserUpdateForm,
    SetPasswordForm,
    PasswordResetForm,
    FriendMgmtForm,
    WorkoutForm,
    CommentForm,
)

# from .forms import Account
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home(request):
    return render(request, "home.html")


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:  # noqa: E722
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
        )
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("homepage")


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "template_activate_account.html",
        {
            "user": user.username,
            "domain": request.get_host(),
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request,
            f"Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox \
            and click on received activation link to confirm \
            and complete the registration.<b>Note:</b> Check your spam folder.",
        )
    else:
        messages.error(
            request,
            f"Problem sending email to {to_email}, check if you typed it correctly.",
        )


@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get("email"))
            return redirect("homepage")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request, template_name="register.html", context={"form": form}
    )


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homepage")


@user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        # public_key = settings.RECAPTCHA_PUBLIC_KEY
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"Hello <b>{user.username}</b>! You have been logged in"
                )
                return redirect("homepage")

        else:
            for key, error in list(form.errors.items()):
                if key == "captcha" and error[0] == "This field is required.":
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue

                messages.error(request, error)

    form = UserLoginForm()

    return render(request=request, template_name="login.html", context={"form": form})


@login_required
def password_change(request):
    user = request.user
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect("login")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, "password_reset_confirm.html", {"form": form})


@user_not_authenticated
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data["email"]
            associated_user = (
                get_user_model().objects.filter(Q(email=user_email)).first()
            )
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string(
                    "template_reset_password.html",
                    {
                        "user": associated_user,
                        "domain": request.get_host(),
                        "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                        "token": account_activation_token.make_token(associated_user),
                        "protocol": "https" if request.is_secure() else "http",
                    },
                )
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(
                        request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered.  # noqa: E501
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address
                            you registered with, and check your spam folder.
                        </p>
                        """,
                    )
                else:
                    messages.error(
                        request,
                        "Problem sending reset password email, <b>SERVER PROBLEM</b>",
                    )

            return redirect("homepage")

        for key, error in list(form.errors.items()):
            if key == "captcha" and error[0] == "This field is required.":
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, template_name="password_reset.html", context={"form": form}
    )


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:  # noqa: E722
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Your password has been set. You may go ahead and <b>log in </b> now.",  # noqa: E501
                )
                return redirect("homepage")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, "password_reset_confirm.html", {"form": form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, "Something went wrong, redirecting back to Homepage")
    return redirect("homepage")


@login_required
def profile(request, username):
    if request.method == "POST":
        if "update_description" in request.POST:
            user = request.user
            form = UserUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                user_form = form.save()
                messages.success(
                    request, f"{user_form.username}, Your profile has been updated!"
                )
                return redirect("profile", user_form.username)

            for error in list(form.errors.values()):
                messages.error(request, error)
        elif "add_friends" in request.POST:
            form = FriendMgmtForm(request.POST)
            if form.is_valid():
                friend_username = form.cleaned_data["friend_username"]
                if (
                    models.CustomUser.objects.filter(username=friend_username).first()
                    is not None
                ):
                    obj = models.FriendMgmt(
                        from_user=request.user,
                        to_user=models.CustomUser.objects.filter(
                            username=friend_username
                        ).first(),
                    )
                    if not models.FriendMgmt.objects.filter(
                        from_user=request.user,
                        to_user=models.CustomUser.objects.filter(
                            username=friend_username
                        ).first(),
                    ).exists():
                        obj.save()
                return HttpResponseRedirect("/profile/" + username)
    else:
        friendsform = FriendMgmtForm()
    created_events = models.Event.objects.filter(created_by=username)
    bookmarked_events = models.BookmarkEvent.objects.filter(user=request.user)
    user = get_user_model().objects.filter(username=username).first()
    if user:
        update_profile_form = UserUpdateForm(instance=user)
        update_profile_form.fields["description"].widget.attrs = {"rows": 1}
        friends1 = models.FriendMgmt.objects.filter(from_user=request.user)
        return render(
            request=request,
            template_name="profile.html",
            context={
                "form": update_profile_form,
                "friends": {"form": friendsform, "friends_list": friends1},
                "created_events": created_events,
                "bookmarked_events": bookmarked_events,
                "page_user": user,
            },
        )

    return redirect("homepage")


"""
@login_required
def profile_alt(request, username):
    user_page = User.objects.get(username=username)
    user_account = Account.objects.get(user=user_page)
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
                if (
                    models.User.objects.filter(username=friend_username).first()
                    is not None
                ):
                    obj = models.FriendMgmt(
                        user=request.user,
                        friend=models.User.objects.filter(
                            username=friend_username
                        ).first(),
                    )
                    if not models.FriendMgmt.objects.filter(
                        user=request.user,
                        friend=models.User.objects.filter(
                            username=friend_username
                        ).first(),
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
            {
                "friends": {"form": form, "friends_list": friends1},
                "user_page": user_page,
                "user_account": user_account,
            },
        )
    else:
        return render(
            request,
            "account/profile.html",
            {"user_page": user_page, "user_account": user_account},
        )
"""


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
            friends_invited = form.data.get("friends_invited")
            event_title = form.cleaned_data.get("title")
            # print("frinds invited ", friends_invited)
            friends_list = friends_invited.split(" ")
            # print(type(friends_list))
            form.save(commit=True)
            for friend_username in friends_list:
                print(friend_username)
                if (
                    models.CustomUser.objects.filter(username=friend_username).first()
                    is not None
                ):
                    event = models.Event.objects.get(title=event_title)
                    obj = models.EventFriendMgmt(
                        event=event,
                        friend=models.CustomUser.objects.filter(
                            username=friend_username
                        ).first(),
                    )
                    print("Event:", event.title)
                    print(
                        "Friend",
                        models.CustomUser.objects.filter(
                            username=friend_username
                        ).first(),
                    )
                    obj.save()

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
        obj_invited = []
    else:
        obj_invited = models.EventFriendMgmt.objects.order_by("id").filter(
            friend=request.user
        )

    if request.user.is_anonymous:
        context = {"obj1": obj_private, "obj2": obj_public}
    else:
        bookmarked_events = models.BookmarkEvent.objects.filter(
            user=request.user
        ).values_list("event", flat=True)
        context = {
            "obj1": obj_private,
            "obj2": obj_public,
            "obj3": obj_invited,
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
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            body = request.POST.get("body")
            new_comment = Comment.objects.create(
                post=post, name=request.user, body=body
            )
            new_comment.save()
            comment_form = CommentForm()

    else:
        comment_form = CommentForm()
    context = {
        "obj1": obj,
        "post": post,
        "comments": comments,
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


def remove_friend(request):
    # print(request.body)
    data = json.loads(request.body)
    friend_username = data["friend_username"]
    # print("Friend Username:", friend_username)
    user = request.user
    friend = models.CustomUser.objects.filter(username=friend_username).first()
    if user != friend:
        # print("friend user object", friend)
        friend1 = models.FriendMgmt.objects.get(from_user=request.user, to_user=friend)
        # print("Friend management object user", friend1.from_user)
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
    print("\n\nIN POST\n\n")
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
    obj = models.Workout.objects.order_by("id").latest("id")
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


"""
DISCUSSION FORUM VIEWS
"""


def forum(request):
    context = {"posts": Post.objects.all()}
    return render(request, "discforum/forum.html", context)


class PostListView(ListView):
    model = Post
    template_name = "discforum/forum.html"  # <app>/<model>_<viewtype>.html <- default template for class-based views, if template_name not specified # noqa: E501
    context_object_name = "posts"
    ordering = ["-date_posted"]


class PostDetailView(DetailView):
    model = Post
    template_name = "discforum/post_detail.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "discforum/post_form.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "discforum/post_form.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "discforum/post_confirm_delete.html"
    success_url = "/post"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
