from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile, User
from post.models import Post
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def sendmail(users, user):

    mail_subject = "Smart Find"
    message = render_to_string('smartFind.html', {
        'users': users,
        'user': user,
    })

    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.send()


class Command(BaseCommand):

    def handle(self, *args, **options):

        posts = Post.objects.filter(expires_at=datetime.now())

        for p in posts:
            postCat = p.categoryID
            users = User.objects.filter(userID__usercategories__categoryID=postCat)
            user = User.objects.get(pk=p.userID)

            if users.count():
                sendmail(users, user)
