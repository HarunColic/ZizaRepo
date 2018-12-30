from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile, User
from post.models import Post
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives


class Command(BaseCommand):

    def handle(self, *args, **options):

        posts = Post.objects.filter(title=' ').filter(type=1)

        for p in posts:

            p.title = p.categoryID.name + "-" + p.position
