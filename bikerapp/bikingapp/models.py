from django.db import models

# Create your models here.

class Event(models.Model):
    location = models.CharField(max_length = 200)
    date_time = models.DateTimeField('event date and time')
    date_created = models.DateTimeField('event created date')
    public_private = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    created_by = models.CharField(max_length = 100, default = 'user')
    