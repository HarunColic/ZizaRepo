from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import pytz


class Category(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=datetime.now)


class Post(models.Model):

    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100)
    url = models.CharField(max_length=100, null=True)
    type = models.IntegerField(db_index=True)
    b2b_type = models.IntegerField(null=True)
    experience = models.IntegerField(default=1)
    contact_email = models.CharField(max_length=100, null=True)
    contact_phone = models.CharField(max_length=50, null=True)
    attachment = models.FileField(null=True)
    content = models.TextField()
    expires_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    soft_delete = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    @property
    def is_past_due(self):
        utc = pytz.UTC
        today = timezone.now()
        exp = self.expires_at

        return today > exp

    @property
    def count_users(self):
        return WorkersPosts.objects.filter(postID=self.pk).count()



class Tag(models.Model):

    tag = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)


class WorkersPosts(models.Model):

    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class PostTags(models.Model):

    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    tagID = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class PostCategories(models.Model):

    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class UserCategories(models.Model):

    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class FAQ(models.Model):

    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
