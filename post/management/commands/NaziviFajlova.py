from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile, User
from post.models import Post
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from post.models import Category
from django.template.defaultfilters import slugify


class Command(BaseCommand):

    def handle(self, *args, **options):

        userPs = UserProfile.objects.all()
        oglasi = Post.objects.all()

        for u in userPs:

            if u.cv:
                u.cv.name = slugify(u.cv.name)

        for o in oglasi:

            if o.attachment:
                o.attachment.name = slugify(o.attachment.name)

