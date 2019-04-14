from django.db import models
from datetime import datetime
from django.utils import timezone


class Region(models.Model):

    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)


class City(models.Model):

    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    regionID = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
