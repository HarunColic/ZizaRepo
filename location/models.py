from django.db import models
from datetime import datetime


class City(models.Model):

    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now())
