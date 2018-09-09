from django.db import models
from datetime import datetime
from django.utils import timezone


class City(models.Model):

    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
