from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from post.models import Category
from location.models import City


class UserProfile(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    verified = models.BooleanField(default=False)
    smart_find = models.BooleanField(default=True)
    image = models.ImageField(null=True)
    location = models.CharField(max_length=255, null=True)
    cv = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)
    brojtelefona = models.CharField(max_length=20, null=True)
    editovanProfil = models.BooleanField(default=False)


class Employee(models.Model):

    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    editovanProfil = models.BooleanField(default=False)
    strucnaSprema = models.CharField(max_length=100, null=True)
    obrazovanje = models.CharField(max_length=200, null=True)
    radnoMjesto = models.CharField(max_length=200, null=True)
    iskustvo = models.IntegerField(null=True)


class Company(models.Model):

    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    company_number = models.CharField(max_length=50)
    brojuposlenih = models.IntegerField(null=True)
    opis = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    web = models.CharField(max_length=1000, null=True)

