from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from post.models import Industry
from django.utils import timezone


class UserProfile(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    verified = models.BooleanField(default=False)
    smart_find = models.BooleanField(default=True)
    image = models.ImageField(null=True)
    location = models.CharField(max_length=1000, null=True)
    cv = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)
    brojtelefona = models.CharField(max_length=20, null=True)

class Employee(models.Model):

    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Company(models.Model):

    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    industryID = models.ForeignKey(Industry, on_delete=models.CASCADE)
    company_number = models.CharField(max_length=50)
    brojuposlenih = models.IntegerField(null=True)
    opis = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

