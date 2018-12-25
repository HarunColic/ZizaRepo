from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile, User
from post.models import Post
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives


class Command(BaseCommand):

    def handle(self, *args, **options):

        users = User.objects.all()

        mail_subject = 'Svima koji slave sretan Božić i Nova godina!'
        message = render_to_string('BozicniMail.html')

        for u in users:
            email = EmailMultiAlternatives(mail_subject, message, to=[u.email])
            email.attach_alternative(message, "text/html")
            email.send()

