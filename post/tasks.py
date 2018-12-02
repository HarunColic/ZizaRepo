from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
from post.models import Post
from django.contrib.auth.models import User
from account import views as AC_Views
from account.models import Employee
from post.models import UserCategories
from post.models import PostCategories
from celery import Celery
from celery.schedules import crontab



def sendExpMail(user, recipientMail, users):

    current_site = get_current_site(request)
    mail_subject = "Smart Find"
    message = render_to_string('smartFind.html', {
        'user': user,
        'users': users,
    })

    email = EmailMessage(
        mail_subject, message, to=[recipientMail]
    )

    email.send()

@periodic_task
def expire():

    posts = Post.objects.all()

    for p in posts:
        if datetime.now() == p.expires_at:
            user = User.objects.get(pk=p.userID)
            postCat = PostCategories.objects.filter(postID=p)
            cat = UserCategories.objects.filter(pk=postCat.categoryID)
            users = Employee.objects.all().filter(cat.userID)

            sendExpMail(user, user.email, users)

            p.soft_delete = True
            p.save()
