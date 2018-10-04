from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from account.models import Company, Employee, UserProfile
from location.models import City
from post.models import Category
from django.contrib.auth import logout, login
from post.models import Post, WorkersPosts
from django.db.models import Q
import re
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponseRedirect
from datetime import datetime
import sweetify
from django.template.context_processors import csrf


def superUser(user):

    if user.email == "ziza@1blackmoon.com":
        return True
    else:
        return False


def validation(request, args):

    for i in args:
        if i == "" or i is None:
            sweetify.error(request, title="Sva polja su obavezna", text="", icon="error", timer=10000)
            return False

    return True


def home(request):

    posts = Post.objects.order_by('created_at')[0:4]

    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)
        return render(request, 'index.html', {'user': request.user, 'auth': True, 'userP': userP, 'industries': None, 'posts': posts})
    else:
        industries = Category.objects.filter(type=0)
        return render(request, 'index.html', {'user': None, 'userP': None, 'auth': False, 'industries': industries, 'posts': posts})


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
                cat = Category.objects.get(name=kategorija)
                posts = posts.all().filter(CategoryID=cat)
            if kljucnaRijec is not None:
                posts = posts.all().filter(Q(title__contains=kljucnaRijec) | Q(content__contains=kljucnaRijec))

        else:
            posts = Post.objects.all().filter(type=1)

        user = request.user
        userP = UserProfile.objects.get(userID=user)
        data = posts
        gradovi = City.objects.all()
        cat = Category.objects.filter(type=0)
        counter = posts.count()
        company = Company.objects.get(userID=user)

        if Company.objects.filter(userID=user).exists():

            userComp = Company.objects.get(userID=user)

            if userComp.categoryID.name == "Finansijske":

                posts = Post.objects.all().filter(userID=user).exclude(expires_at__lte=datetime.now()).exclude(categoryID__name="Osiguravajuće")
                return render(request, 'profilTvrtka.html', {'user': user, 'userP': userP, 'company': company, 'posts': posts})

            elif userComp.categoryID.name == "Finansijske":

                posts = Post.objects.all().filter(userID=user).exclude(expires_at__lte=datetime.now()).exclude(categoryID__name="Finansijske")
                return render(request, 'profilTvrtka.html',
                              {'user': user, 'userP': userP, 'company': company, 'posts': posts})
            elif superUser(request.user):
                posts = Post.objects.all().filter(userID=user).exclude(expires_at__lte=datetime.now())
                return render(request, 'profilTvrtka.html',
                              {'user': user, 'userP': userP, 'company': company, 'posts': posts})
            else:
                posts = Post.objects.all().filter(type=2).exclude(categoryID__name="Finansijske").exclude(
                    categoryID__name="Osiguravajuće").exclude(expires_at__lte=datetime.now())
                return render(request, 'profilTvrtka.html',
                          {'user': user, 'userP': userP, 'company': company, 'posts': posts})

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

                args = [user.first_name, user.last_name, user.email, lozinka]

                if not validation(request, args):
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                if len(lozinka) < 6:
                    sweetify.sweetalert(request, button=True, title="Lozinka mora biti 6 ili više karaktera", icon="error", timer=10000)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                elif not validateMail(user.email):
                        sweetify.sweetalert(request,button=True, title="Unesite validnu email adresu", icon="error", timer=10000)
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                if User.objects.filter(email=user.email).exists():
                    sweetify.sweetalert(request, title="Email adresa već postoji", text="Već postoji korisnik sa ovom email adresom, ako ste zaboravili lozinku molimo kliknite na Forgot password", icon="error", timer=10000)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                elif not validateMail(user.email):
                    sweetify.sweetalert(request, button=True, title="Neispravna Email adresa", text="Molimo unesite ispravnu Email adresu", icon="error", timer=10000)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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

                city.name = city.name.lower()
                city.name = city.name.title()

                if City.objects.filter(name=city.name).exists():
                    city = City.objects.get(name=city.name)
                else:
                    city.save()

                categoryname = request.POST.get('Category', None)
                user.first_name = request.POST['FirstName']
                user.last_name = request.POST['LastName']
                user.email = request.POST['mail']
                user.set_password(request.POST['pswd'])
                user.username = user.last_name + "." + user.email
                lozinka = request.POST['pswd']

                args = [user.first_name, user.last_name, user.email, lozinka, categoryname]

                if not validation(request, args):
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                category = Category.objects.get(name=categoryname)

                if User.objects.filter(email=user.email).exists():
                    sweetify.sweetalert(request, title="Email adresa već postoji", text="Već postoji korisnik sa ovom email adresom, ako ste zaboravili lozinku molimo kliknite na Forgot password", icon="error", timer=10000)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                elif not validateMail(user.email):
                    sweetify.sweetalert(request, title="Neispravna Email adresa", text="Molimo unesite ispravnu Email adresu", icon="error")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                else:
                    user.clean()
                    user.save()

                    comp = Company()
                    comp.userID = user
                    comp.ID_Number = user.last_name
                    comp.categoryID = category
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

    return redirect('pretraga')


def signin(request):

        if request.method == 'POST':

            mail = request.POST['mail']
            password = request.POST['pswd']

            args = [mail, password]

            if not validation(request, args):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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

            if Employee.objects.filter(userID=request.user).exists():
                return redirect('pretraga')
            else:
                return redirect('dashboard')


def signout(request):

    logout(request)
    c = {}
    c.update(csrf(request))
    return redirect('home')


def editprofil(request):

    #edit profil kompanije

    if request.user.is_authenticated:
        user = request.user
        userP = UserProfile.objects.get(userID=user)
        gradovi = City.objects.all()
        comp = Company.objects.get(userID=user)
        cat = Category.objects.filter(type=0)

        return render(request, 'editProfilTvrtka.html', {'user': user, 'gradovi': gradovi, 'userP': userP, 'comp': comp, 'cat': cat})
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
            cat = request.POST.get('category', None)
            brojuposlenika = request.POST['brojuposlenih']
            opis = request.POST['opis']
            slika = request.FILES.get('profilePicture', default=None)

            args = [name, mail, brojtel, grad, cat, brojuposlenika, opis]

            if not validation(request, args):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            user = request.user
            userP = UserProfile.objects.get(userID=user)
            comp = Company.objects.get(userID=user)
            category = Category.objects.get(name=cat)

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
                comp.categoryID = category
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
        return render(request, 'onamanew.html', {'user': request.user, 'auth': auth, 'userP': userP, 'industries': None})
    else:
        auth = False
        industries = Category.objects.filter(type=0)
        return render(request, 'onamanew.html', {'user': request.user, 'auth': auth, 'industries': industries})


def konsalting(request):

    if request.user.is_authenticated:
        user = request.user
        userP = UserProfile.objects.get(userID=user)
        return render(request, 'konsalting.html', {'user': user, 'userP':userP, 'auth': True, 'industries': None})
    else:
        industries = Category.objects.filter(type=0)
        return render(request, 'konsalting.html', {'user': None, 'userP':None, 'auth': False, 'industries': industries})


def pretraga(request):

    auth = False

    if request.user.is_authenticated:

        auth = True

        user = request.user
        userP = UserProfile.objects.get(userID=user)

        if request.POST.get('pretragaTrigger', "False") == "True":
            grad = request.POST.get('gradovi', None)
            kategorija = request.POST.get('kategorije', None)
            kljucnaRijec = request.POST.get('kljucnaRijec', None)

            if Company.objects.filter(userID=user).exists():

                userComp = Company.objects.get(userID=user)
                if userComp.categoryID.name == "Finansijske":
                    posts = Post.objects.all().filter(type=2).exclude().exclude(categoryID__name="Osiguravajuće").exclude(expires_at__lte=datetime.now())
                elif userComp.categoryID.name == "Osiguravajuće":
                    posts = Post.objects.all().filter(type=2).exclude().exclude(categoryID__name="Finansijske").exclude(expires_at__lte=datetime.now())
                elif superUser(request.user):
                    posts = Post.objects.all().exclude(expires_at__lte=datetime.now())
                else:
                    posts = Post.objects.all().filter(type=2).exclude(categoryID__name="Finansijske").exclude(categoryID__name="Osiguravajuće").exclude(expires_at__lte=datetime.now())
            else:
                posts = Post.objects.filter(type=1).exclude(expires_at__lte=datetime.now())

            if grad is not None:
                posts = posts.filter(location=grad)
            if kategorija is not None:
                ind = Category.objects.get(name=kategorija)
                posts = posts.filter(categoryID=ind)
            if kljucnaRijec is not "":
                posts = posts.filter(Q(title__contains=kljucnaRijec) | Q(content__contains=kljucnaRijec))

        else:
            if Company.objects.filter(userID=user).exists():
                posts = Post.objects.all().filter(type=2)
            else:
                posts = Post.objects.all().filter(type=1)

        data = posts.exclude(expires_at__lte= datetime.now())

        userP = UserProfile.objects.get(userID=user)
        gradovi = City.objects.all()
        cat = Category.objects.filter(type=1)
        counter = data.count()
        users = User.objects.all()
        userPs = UserProfile.objects.all()
        btb = ["Ponuda", "Potražnja", "Partnerstvo"]
        return render(request, 'pretrazi.html',
                      {'user': user, 'data': data, 'gradovi': gradovi, 'cat': cat, 'userP': userP, 'auth': auth, 'counter': counter, 'users': users, 'userPs': userPs, 'btb': btb})
    else:
        return redirect('home')


def dashboard(request):

    if request.user.is_authenticated:

        if Company.objects.filter(userID=request.user).exists():

            userP = UserProfile.objects.get(userID=request.user)
            activePosts = Post.objects.filter(userID=request.user).exclude(soft_delete=True)
            inactivePosts = Post.objects.filter(userID=request.user).exclude(soft_delete=False)
            company = Company.objects.get(userID=request.user)
            relevantPosts = Post.objects.filter(categoryID=company.categoryID)

            return render(request, 'dashboard.html', {'user': request.user, 'userP': userP, 'auth': True, 'ind': None, 'activepPosts': activePosts, 'inactivePosts': inactivePosts, 'relevantPosts': relevantPosts})
        else:
            return HttpResponseRedirect(request.META.get('HTTP_RENDERER', '/'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_RENDERER', '/'))


def testPretraga(request):

    auth = False

    if request.user.is_authenticated:

        auth = True

        user = request.user
        userP = UserProfile.objects.get(userID=user)

        if request.POST.get('pretragaTrigger', "False") == "True":
            grad = request.POST.get('gradovi', None)
            kategorija = request.POST.get('kategorije', None)
            kljucnaRijec = request.POST.get('kljucnaRijec', None)

            if Company.objects.filter(userID=user).exists():

                userComp = Company.objects.get(userID=user)
                if userComp.categoryID.name == "Finansijske":
                    posts = Post.objects.all().filter(type=2).exclude().exclude(
                        categoryID__name="Osiguravajuće").exclude(expires_at__lte=datetime.now())
                elif userComp.categoryID.name == "Osiguravajuće":
                    posts = Post.objects.all().filter(type=2).exclude().exclude(categoryID__name="Finansijske").exclude(
                        expires_at__lte=datetime.now())
                elif superUser(request.user):
                    posts = Post.objects.all().exclude(expires_at__lte=datetime.now())
                else:
                    posts = Post.objects.all().filter(type=2).exclude(categoryID__name="Finansijske").exclude(
                        categoryID__name="Osiguravajuće").exclude(expires_at__lte=datetime.now())
            else:
                posts = Post.objects.filter(type=1).exclude(expires_at__lte=datetime.now())

            if grad is not None:
                posts = posts.filter(location=grad)
            if kategorija is not None:
                ind = Category.objects.get(name=kategorija)
                posts = posts.filter(categoryID=ind)
            if kljucnaRijec is not "":
                posts = posts.filter(Q(title__contains=kljucnaRijec) | Q(content__contains=kljucnaRijec))

        else:
            if Company.objects.filter(userID=user).exists():
                posts = Post.objects.all().filter(type=2)
            else:
                posts = Post.objects.all().filter(type=1)

        data = posts.exclude(expires_at__lte=datetime.now())

        userP = UserProfile.objects.get(userID=user)
        gradovi = City.objects.all()
        cat = Category.objects.filter(type=1)
        counter = data.count()
        users = User.objects.all()
        userPs = UserProfile.objects.all()
        btb = ["Ponuda", "Potražnja", "Partnerstvo"]
        return render(request, 'pretrazi.html',
                      {'user': user, 'data': data, 'gradovi': gradovi, 'cat': cat, 'userP': userP, 'auth': auth,
                       'counter': counter, 'users': users, 'userPs': userPs, 'btb': btb})
    else:
        return redirect('home')
