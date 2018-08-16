from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Employee(models.Model):

    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now())


class Company(models.Model):

    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    company_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.now())

