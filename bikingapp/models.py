from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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


class Workout(models.Model):
    title = models.CharField(max_length=50)
    miles = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=500, null=True)
    created_by = models.CharField(max_length=100, default="user")

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
class Comment(models.Model):
    post = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='comments')
    name= models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    #name = models.CharField(max_length=80)
    #email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
