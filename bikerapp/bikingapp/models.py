from django.db import models
from django.utils import timezone
# Create your models here.

class Event(models.Model):
    location       = models.CharField     (max_length = 200)
    date           = models.DateField     (default=timezone.now)
    time           = models.TimeField     (default=timezone.now)
    date_created   = models.DateTimeField (default=timezone.now)
    event_type     = models.CharField     (max_length = 200, choices=[("public","Public"),("public","Private")], default="Public")
    description    = models.CharField     (max_length = 500)
    created_by     = models.CharField     (max_length = 100, default = 'user')
    