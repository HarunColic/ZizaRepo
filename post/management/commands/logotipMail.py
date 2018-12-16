from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile, User
from post.models import Post
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from post.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        userPs = UserProfile.objects.filter(image='')
        mails = []

        for up in userPs:

            this = User.objects.get(userprofile=up)
            mails.append(this.email)

        mail_subject = "Mailovi korisnika bez logotipa"
        message = render_to_string('MailoviBezLogotipa.html', {

            'mails': mails,

        })

        email = EmailMessage(
            mail_subject, message, to=['affan@ziza.ba']
        )

        email.send()
