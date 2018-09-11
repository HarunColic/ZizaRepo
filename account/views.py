from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from account.models import Company, Employee, UserProfile
from location.models import City
from post.models import Industry, Category
from django.contrib.auth import logout, login
from post.models import Post
from django.db.models import Q
import re
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
import sweetify
from django.http import HttpResponseRedirect


def home(request):

    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)
        return render(request, 'home.html', {'user': request.user, 'auth': True, 'userP': userP})
    else:
        return render(request, 'index.html', {'user': None, 'userP': None, 'auth': False})


def profil(request):

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
        userP = UserProfile.objects.get(userID=user)
        data = posts
        gradovi = City.objects.all()
        cat = Category.objects.all()
        counter = posts.count()
        company = Company.objects.get(userID=user)

        if Company.objects.filter(userID=user).exists():
            posts = Post.objects.all().filter(userID=user)
            return render(request, 'profilTvrtka.html', {'user': user, 'userP': userP, 'company': company, 'posts': posts})
        elif Employee.objects.filter(userID=user).exists():
            return render(request, 'pretrazi.html', {'user': user, 'data': data, 'counter': counter, 'gradovi': gradovi, 'cat': cat, 'userP': userP})
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
            lozinka = request.POST['pswd']

            if len(lozinka) < 6:
                sweetify.sweetalert(request, title="Lozinka mora biti 6 ili više karaktera", icon="error", timer=10000)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            elif not validateMail(user.email):
                    sweetify.sweetalert(request, title="Unesite validnu email adresu", icon="error", timer=10000)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            if User.objects.filter(email=user.email).exists():
                sweetify.sweetalert(request, title="Email adresa već postoji", text="Već postoji korisnik sa ovom email adresom, ako ste zaboravili loyinku molimo kliknite na 'Forgot password'", icon="error", timer=10000)
                return redirect('home')
            else:

                if validateMail(user.email):

                    user.clean()
                    user.save()

                    emp = Employee(userID=user)
                    emp.save()

                    userP = UserProfile(userID=user)
                    userP.save()

                    sendmail(request, user, user.email)

                    sweetify.success(request, 'Uspješna registracija', text=' molimo verifikujte svoj mail', icon="success", timer=10000)

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
               return redirect('home')
            else:
                user.clean()
                user.save()

                comp = Company()
                comp.userID = user
                comp.ID_Number = user.last_name
                comp.industryID = industry
                comp.clean()
                comp.save()

                userP = UserProfile(userID=user, location=city.name)
                userP.save()

                sendmail(request, user, user.email)

                sweetify.success(request, 'Uspješna registracija', text=' molimo verifikujte svoj mail', icon="success",timer=10000)

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

        if User.objects.filter(email=mail).exists():
            user = User.objects.get(email=mail)
        else:
            sweetify.sweetalert(request, title="Korisnik ne postoji", text="Korisnik sa unesenom email adresom ne postoji", icon="error", timer=10000)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        if user.check_password(password):
            if UserProfile.objects.get(userID=user).verified:
                login(request, user)
            else:
                sweetify.error(request, 'Mail nije verifikovan', text='Molimo potvrdite svoju registraciju klikom na link u mailu', icon="error", timer=10000)

    return redirect('profil')


def signout(request):

    logout(request)
    return redirect('home')


def editprofil(request):

#edit profil kompanije

    if request.user.is_authenticated:
        user = request.user
        userP = UserProfile.objects.get(userID=user)
        gradovi = City.objects.all()
        ind = Industry.objects.all()
        comp = Company.objects.get(userID=user)

        return render(request, 'editProfilTvrtka.html', {'user': user, 'gradovi': gradovi, 'ind': ind, 'userP': userP, 'comp': comp})
    else:
        redirect('home')

#potrebno dodati edit profil osobe


def submitchange(request):

    if request.user.is_authenticated:

        if request.method == "POST":
            name = request.POST['naslov']
            mail = request.POST['email']
            brojtel = request.POST['brojTel']
            grad = request.POST['city']
            indust = request.POST['industry']
            brojuposlenika = request.POST['brojuposlenih']
            opis = request.POST['opis']
            slika = request.FILES.get('profilePicture', default=None)

            user = request.user
            userP = UserProfile.objects.get(userID=user)
            comp = Company.objects.get(userID=user)
            djelatnost = Industry.objects.get(name=indust)

            if validateMail(mail):

                usermail = True

                if mail != user.email:
                    usermail = False

                    if User.objects.filter(email=mail).exists():
                        sweetify.error(request, 'Mail već postoji',
                                       text='molimo izaberite novi mail', icon="error",
                                         timer=10000)
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                user.first_name = name
                user.email = mail
                userP.location = grad
                userP.brojtelefona = brojtel
                if slika:
                    userP.image = slika
                comp.industryID = djelatnost
                comp.brojuposlenih = brojuposlenika
                comp.opis = opis

                user.save()
                userP.save()
                comp.save()

                if usermail is False:

                    sweetify.success(request, 'Molimo verifikujte svoj mail', icon="success", timer=10000)
                    sendmail(request, user, mail)
                    logout(request)

            else:
                sweetify.error(request, 'Mail nije validan',
                               text='molimo unesite validnu email adresu', icon="error",
                               timer=10000)

    return redirect('profil')


def onama(request):


    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)
        auth = True
        return render(request, 'onamanew.html', {'user': request.user, 'auth': auth, 'userP': userP})
    else:
        auth = False
        return render(request, 'onamanew.html', {'user': request.user, 'auth': auth})


def pretraga(request):

    auth = False

    if request.user.is_authenticated:

        auth = True

        user = request.user

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
            if Company.objects.filter(userID=user).exists():
                posts = Post.objects.all().filter(type=2)
            else:
                posts = Post.objects.all().filter(type=1)

        data = posts

        userP = UserProfile.objects.get(userID=user)
        gradovi = City.objects.all()
        cat = Category.objects.all()
        counter = posts.count()
        return render(request, 'pretrazi.html',
                      {'user': user, 'data': data, 'gradovi': gradovi, 'cat': cat, 'userP': userP, 'auth': auth, 'counter': counter})
    else:
        return redirect('home')