from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from account.models import Company, Employee, UserProfile
from location.models import City
from post.models import Industry, Category
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from post.models import Post
from post.models import UserCategories, PostCategories
from django.db.models import Q
import re
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text


def home(request):

    if request.user.is_authenticated:

        if request.POST.get('pretragaTrigger', "False") == "True":
            grad = request.POST.get('gradovi', None)
            kategorija = request.POST.get('kategorije', None)
            kljucnaRijec = request.POST.get('kljucnaRijec', None)

            posts = Post.objects.all().filter(type=1)

            if grad is not None:
                posts = posts.all().filter(location=grad)
            if kategorija is not None:
                ind = Industry.objects.get(name=kategorija)
                posts = posts.all().filter(industryID=ind)
            if kljucnaRijec is not None:
                posts = posts.all().filter(Q(title__contains=kljucnaRijec) | Q(content__contains=kljucnaRijec))

        else:
            posts = Post.objects.all().filter(type=1)

        user = request.user
        userP = UserProfile.objects.all()
        data = posts
        gradovi = City.objects.all()
        cat = Category.objects.all()
        counter = posts.count()
        return render(request, 'logiran.html', {'user': user, 'data': data, 'counter': counter, 'gradovi': gradovi, 'cat': cat, 'userP': userP})
    else:
        return render(request, 'index.html')


def validateMail(mail):

    if re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail):
        return True
    else:
        return False


def sendmail(request, user, recipientMail):

    current_site = get_current_site(request)
    mail_subject = "Aktiviraj svoj racun"
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    email = EmailMessage(
        mail_subject, message, to=[recipientMail]
    )

    email.send()


def register(request):

    if request.method == 'POST':
        if request.POST['vrsta'] == "radnik":

            user = User()

            user.first_name = request.POST['FirstName']
            user.last_name = request.POST['LastName']
            user.email = request.POST['mail']
            user.set_password(request.POST['pswd'])
            user.username = user.last_name + "." + user.email

            if User.objects.filter(email=user.email).exists():
                redirect('home')
            else:

                if validateMail(user.email):

                    user.clean()
                    user.save()

                    emp = Employee(userID=user)
                    emp.save()

                    userP = UserProfile(userID=user)
                    userP.save()

                    sendmail(request, user, user.email)

            return redirect('home')

        else:

            user = User()
            city = City(name=request.POST['City'])
            industry = Industry()

            city.name = city.name.lower()
            city.name = city.name.title()

            if City.objects.filter(name=city.name).exists():
                city = City.objects.get(name=city.name)
            else:
                city.save()

            industry.name = request.POST['Industry']

            industry.name = industry.name.lower()
            industry.name = industry.name.title()

            if Industry.objects.filter(name=industry.name):
                industry = Industry.objects.get(name=industry.name)
            else:
                industry.save()

            user.first_name = request.POST['FirstName']
            user.last_name = request.POST['LastName']
            user.email = request.POST['mail']
            user.set_password(request.POST['pswd'])
            user.username = user.last_name + "." + user.email

            if User.objects.filter(email=user.email).exists():
                redirect('home')
            else:
                user.clean()
                user.save()

                comp = Company()
                comp.userID = user
                comp.ID_Number = user.last_name

                comp.clean()
                comp.save()

                userP = UserProfile(userID=user, location=city.name)
                userP.save()

                sendmail(request, user, user.email)

            return redirect('home')

    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        userP = UserProfile.objects.filter(userID=user).update(verified=True)
        login(request, user)

    return redirect('home')


def signin(request):

    if request.method == 'POST':

        mail = request.POST['mail']
        password = request.POST['pswd']

        user = User.objects.get(email=mail)

        if user.check_password(password):
            if UserProfile.objects.get(userID=user).verified:
                login(request, user)

    return redirect('home')


def signout(request):

    logout(request)
    return redirect('home')
