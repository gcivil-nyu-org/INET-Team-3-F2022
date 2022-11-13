from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='profile')
    pronouns = models.CharField(
        max_length=10,
        choices =  [('He/Him','He/Him'),('She/Her','She/Her'),('They/Them','They/Them')],
    )
    description = models.CharField(max_length=500, default="Enter your description", null=True)

    def __str__(self):
        return str(self.user.username) + str(self.pronouns)

class Event(models.Model):
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    borough = models.CharField(
        max_length=20,
        choices=[
            ("manhattan", "Manhattan"),
            ("queens", "Queens"),
            ("bronx", "Bronx"),
            ("staten island", "Staten Island"),
            ("brooklyn", "Brooklyn"),
        ],
        default="Manhattan",
    )
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)
    event_type = models.CharField(
        max_length=200,
        choices=[("public", "Public"), ("private", "Private")],
        default="Public",
    )
    description = models.CharField(max_length=500, null=True)
    created_by = models.CharField(max_length=100, default="user")
    zipcode = models.CharField(max_length=5, null=True)
    state = models.CharField(max_length=10, default="New York")

    def __str__(self):
        return str(self.description) + str(self.created_by)


class BookmarkEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + str(self.event) + str(self.date_added)


class FriendMgmt(models.Model):
    """
    friends table
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    friend = models.ForeignKey(
        User, related_name="friends", on_delete=models.SET_NULL, null=True, blank=True
    )
