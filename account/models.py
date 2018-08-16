from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class UserProfile(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    verified = models.BooleanField(default=False)
    smart_find = models.BooleanField(default=True)
    image = models.CharField(max_length=1000, null=True)
    location = models.CharField(max_length=1000, null=True)
    cv = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(default=datetime.now())
    deleted = models.BooleanField(default=False)


class Employee(models.Model):

    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now())


class Company(models.Model):

    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    company_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.now())

