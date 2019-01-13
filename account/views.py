from builtins import type
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from account.models import Company, Employee, UserProfile
from location.models import City
from post.models import Category, Exhibition
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
from django.http import HttpResponse
from datetime import datetime
import sweetify
from django.template.context_processors import csrf
from django.utils.crypto import get_random_string
from django.core.urlresolvers import resolve
from post.models import UserCategories
from django.db.models.functions import Length
import  os
from threading import Thread
from itertools import chain
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from django.template.defaultfilters import slugify


def superUser(user):

    if user.email == "ziza@1blackmoon.com":
        return True
    else:
        return False


def validation(request, args):

    for i in args:
        if i == "" or i is None:
            sweetify.error(request, title="Unesite obavezna polja", text="", icon="error", timer=10000)
            return False

    return True


def home(request):

    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    cetriOglasa = Post.objects.filter().exclude(soft_delete=True)[0:4]
    cetriUserP = []

    for cet in cetriOglasa:
        #cetriUserP.append(UserProfile.objects.get(userID=cet.userID))
        cetriUserP.append(None  )

    topOglasi = Post.objects.filter().exclude(soft_delete=True).order_by('views', '-created_at')[0:3]

    if topOglasi.count() == 3:

        topOglasi = list(topOglasi)
        oglas1 = topOglasi[0]
        oglas2 = topOglasi[1]
        oglas3 = topOglasi[2]

        prvaSlika = 'images/pcela_' + str(oglas1.categoryID.slika) + '.png'
        drugaSlika = 'images/pcela_' + str(oglas2.categoryID.slika) + '.png'
        trecaSlika = 'images/pcela_' + str(oglas3.categoryID.slika) + '.png'

    else:
        topOglasi = list(topOglasi)
        oglas1 = None
        oglas2 = None
        oglas3 = None

        prvaSlika = None
        drugaSlika = None
        trecaSlika = None

    postsB2C = Post.objects.filter(type=1).exclude(categoryID__name="Osiguravajuće").exclude(categoryID__name="Finansijske").exclude(soft_delete=True).order_by('-created_at')[0:4]
    postsB2B = Post.objects.filter(type=2).exclude(categoryID__name="Osiguravajuće").exclude(categoryID__name="Finansijske").exclude(soft_delete=True).order_by('-created_at')[0:4]

    if request.user.is_authenticated:
        if Company.objects.filter(userID=request.user).exists():
            usr = 'comp'
        else:
            usr = 'wrkr'
        userP = UserProfile.objects.get(userID=request.user)
        return render(request, 'index.html', {'user': request.user, 'auth': True, 'userP': userP, 'industries': None,
                                              'postsbc': postsB2C, 'postbb':postsB2B, 'oglas1': oglas1, 'oglas2': oglas2,
                                              'oglas3': oglas3, 'cetriOglasa': cetriOglasa, 'cetriUserP': cetriUserP,
                                              'prvaSlika': prvaSlika, 'drugaSlika': drugaSlika, 'trecaSlika': trecaSlika,
                                              'usr': usr})
    else:
        industries = Category.objects.filter(type=0)
        return render(request, 'index.html', {'user': None, 'userP': None, 'auth': False, 'industries': industries,
                                              'postsbc': postsB2C, 'postbb':postsB2B, 'oglas1': oglas1, 'oglas2': oglas2,
                                              'oglas3': oglas3, 'cetriOglasa': cetriOglasa, 'cetriUserP': cetriUserP,
                                              'prvaSlika': prvaSlika, 'drugaSlika': drugaSlika, 'trecaSlika': trecaSlika,
                                              'usr': None})


def profil(request):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)
        user = request.user

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        if Company.objects.filter(userID=user).exists():
            company = Company.objects.get(userID=user)

            postovi = Post.objects.filter(userID=user).exclude(soft_delete=True)

            paginator = Paginator(postovi, 5)
            page = request.GET.get('page', 1)
            posts = paginator.page(page)
            rng = range(1, paginator.num_pages + 1)

            exhibs = Exhibition.objects.filter(userID=request.user)

            exhibPaginator = Paginator(exhibs, 5)
            exhibPage = request.GET.get('pageI', 1)
            izlozi = exhibPaginator.page(exhibPage)
            exRNG = range(1, exhibPaginator.num_pages +1)

            return render(request, 'profilTvrtka.html',
                          {'usr': 'comp', 'auth': True, 'user': user, 'userP': userP, 'company': company, 'posts': posts
                              , 'page': int(page), 'rng': rng, 'izlozi': izlozi, 'exhibPage': int(exhibPage), 'exRNG': exRNG
                              , 'acctype':'f',
                           })

        elif Employee.objects.filter(userID=user).exists():
            emp = Employee.objects.get(userID=user)
            vjestine = UserCategories.objects.filter(userID=user)

            return render(request, 'testprofil.html', {'emp': emp, 'usr': 'wrkr', 'auth': True, 'user': user,
                                                       'userP': userP, 'vjestine': vjestine})
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

    email = EmailMultiAlternatives(
        mail_subject, message, to=[recipientMail]
    )
    email.attach_alternative(message, "text/html")
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

                if len(user.last_name) >= 30:
                    sweetify.sweetalert(request, button=True, title="Prezime mora biti manje od 30 karaktera",
                                        icon="error", timer=10000)
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

                        recipientMail = "affancehajic@gmail.com"

                        mail_subject = "Novi Korisnik"
                        message = render_to_string('AffanReport.html', {'user': user})

                        mailZaAffana = EmailMessage(
                           mail_subject, message, to=[recipientMail]
                        )

                        mailZaAffana.send()

                        sweetify.success(request, 'Uspješna registracija', text=' molimo verifikujte svoj mail', icon="success", timer=10000)

                return redirect('home')

            else:

                user = User()
                grad = request.POST.get('City', None)
                categoryname = request.POST.get('Category', None)
                user.first_name = request.POST.get('FirstName', None)
                user.last_name = request.POST.get('LastName', None)
                user.email = request.POST.get('mail', None)
                user.set_password(request.POST.get('pswd', None))
                user.username = user.last_name + "." + user.email
                lozinka = request.POST['pswd']

                if len(user.first_name) > 100:
                    sweetify.sweetalert(request, title="Naziv firme predug", text="Molimo unesite naziv do 100 karaktera", icon="error", timer=4000)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                if len(user.last_name) >= 30:
                    sweetify.sweetalert(request, button=True, title="Broj firme mora biti manje od 30 karaktera",
                                        icon="error", timer=10000)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                args = [user.first_name, user.last_name, user.email, lozinka, categoryname]

                if not validation(request, args):
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                category = Category.objects.filter(name=categoryname,type=0)[0]

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

                    userP = UserProfile(userID=user, location=grad)
                    userP.save()

                    sendmail(request, user, user.email)

                    recipientMail = "affancehajic@gmail.com"

                    mail_subject = "Novi Korisnik"
                    message = render_to_string('AffanReport.html', {'user': user})

                    mailZaAffana = EmailMessage(
                        mail_subject, message, to=[recipientMail]
                    )

                    mailZaAffana.send()

                    sweetify.success(request, 'Uspješna registracija', text=' molimo verifikujte svoj mail', icon="success",timer=10000)

                return redirect('home')

        return redirect('home')


def sendZahvanicu(request, recipientMail):

    current_site = get_current_site(request)
    mail_subject = "Zahvalnica"
    message = render_to_string('zahvalnica.html', {})

    email = EmailMessage(
        mail_subject, message, to=[recipientMail]
    )

    email.send()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        userP = UserProfile.objects.filter(userID=user).update(verified=True)
        sendZahvanicu(request, user.email)
        login(request, user)

        return redirect('editprofil')


def signin(request):

    if request.user.is_authenticated:
        sweetify.sweetalert(request, title="Već ste prijavljeni", icon="error")
        return redirect('home')

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
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            sweetify.sweetalert(request, title="Pogrešna lozinka", text="", icon="error", timer=1000)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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

    if request.user.is_authenticated:

        if Company.objects.filter(userID=request.user).exists():
            user = request.user
            userP = UserProfile.objects.get(userID=user)
            gradovi = City.objects.all()
            comp = Company.objects.get(userID=user)
            cat = Category.objects.filter(type=0)

            return render(request, 'editProfilTvrtka.html', {'auth': True, 'usr': 'comp', 'user': user, 'gradovi': gradovi, 'userP': userP, 'comp': comp, 'cat': cat})

        elif Employee.objects.filter(userID=request.user).exists():
            user = request.user
            userP = UserProfile.objects.get(userID=user)
            gradovi = City.objects.all()
            emp = Employee.objects.get(userID=user)
            cat = Category.objects.filter(type=4)
            userCats = UserCategories.objects.filter(userID=user)
            catNames = []

            for c in cat:
                catNames.append(c.name)

            return render(request, 'editProfilPL.html', {'catNames': catNames, 'userCats': userCats, 'auth': True, 'usr': 'wrkr', 'user': user, 'gradovi': gradovi, 'userP': userP, 'emp': emp, 'cat': cat})

    else:
        redirect('home')


def submitchange(request):

    # - * - coding: utf - 8 -*-

    if request.user.is_authenticated:

        if Company.objects.filter(userID=request.user).exists():

            if request.method == "POST":
                name = request.POST['naslov']
                mail = request.POST['email']
                brojtel = request.POST['brojTel']
                grad = request.POST['City']
                cat = request.POST.get('category', None)
                brojuposlenika = request.POST['brojuposlenih']
                opis = request.POST['opis']
                slika = request.FILES.get('profilePicture', default=None)
                webStranica = request.POST.get('webStranica', None)
                izvjestaj = request.FILES.get('finIzvjestaj', None)
                args = [name, mail, brojtel, grad, cat, brojuposlenika, opis]
                if not validation(request, args):
                    sweetify.sweetalert(request, title="Sva polja obavezna", icon="error")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                user = request.user
                userP = UserProfile.objects.get(userID=user)
                comp = Company.objects.get(userID=user)
                category = Category.objects.filter(name=cat)[0]

                if validateMail(mail):

                    usermail = True

                    if mail != user.email:
                        usermail = False

                        if User.objects.filter(email=mail).exists():
                            sweetify.error(request, 'Mail već postoji',
                                           text='molimo izaberite novi mail', icon="error",
                                             timer=10000)
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


                        fs = FileSystemStorage()
                        filename = fs.save(izvjestaj.name, izvjestaj)
                        uploaded_file_url = fs.url(filename)

                    if izvjestaj is not None:
                        if izvjestaj._size > 5242880:
                            sweetify.sweetalert(request, title="Datoteka prevelika",text="Vaša datoteka prelazi maksimalnu veličinu od 5 MB", icon="error",timer=10000)
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                    user.first_name = name
                    user.email = mail
                    userP.location = grad
                    userP.brojtelefona = brojtel
                    if slika:
                        userP.image = slika
                    elif not userP.image:
                        sweetify.sweetalert(request, title="Molimo dodajte sliku", icon="error")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                    comp.categoryID = category
                    comp.brojuposlenih = brojuposlenika
                    comp.opis = opis

                    if webStranica:
                        comp.web = webStranica

                    user.save()
                    userP.editovanProfil = True
                    userP.cv = izvjestaj
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
        else:

            if request.method == "POST":
                name = request.POST.get('naslov', default=None)
                radnoMjesto = request.POST.get('radno', default=None)
                email = request.POST.get('email', default=None)
                iskustvo = request.POST.get('iskustvo', default= None)
                kontaktBroj = request.POST.get('brojTel', None)
                grad = request.POST.get('grad', default=None)
                opis = request.POST.get('opis', default=None)
                slika = request.FILES.get('profilePicture', None)
                kategorije = request.POST.get('kkk').split(',')
                strucnaSprema = request.POST.get('strucnaSprema', default=None)
                obrazovanje = request.POST.get('obrazovanje', default=None)

                if iskustvo is None or iskustvo == '':
                    iskustvo = 0

                myfile = request.FILES.get('image_uploads', None)

                if myfile is not None:

                    splitovano = myfile.name.split(".")

                    myfile.name = slugify(str(datetime.now()) + "." + splitovano[splitovano.__len__()-1])
                    fs = FileSystemStorage()

                    filename = fs.save(myfile.name, myfile)
                    uploaded_file_url = fs.url(filename)

                args = [email, name, grad, kontaktBroj, opis, strucnaSprema, obrazovanje]

                if not validation(request, args):
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                imeiPrezime = name.split()
                ime = imeiPrezime[0]
                prezime = imeiPrezime[1]

                user = request.user

                user.first_name = ime
                user.last_name = prezime

                emp = Employee.objects.get(userID=request.user)
                emp.strucnaSprema=strucnaSprema
                emp.obrazovanje = obrazovanje
                emp.iskustvo = iskustvo
                emp.opis = opis

                userP = UserProfile.objects.get(userID=request.user)

                if myfile is not None:
                    if myfile._size > 5242880:
                        sweetify.sweetalert(request, title="Datoteka prevelika",text="Vaš CV prelazi maksimalnu veličinu od 5 MB", icon="error",timer=10000)
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                    userP.cv = myfile

                userP.location = grad
                userP.brojtelefona = kontaktBroj

                if radnoMjesto is not None or radnoMjesto == '':
                    emp.radnoMjesto = radnoMjesto
                if slika is not None:
                    try:
                        userP.image = slika
                    except IOError:
                        sweetify.sweetalert(request, title='Slika nije validna', icon='error')
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                elif not userP.image:
                    sweetify.sweetalert(request, title="Molimo dodajte sliku", icon="error")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                if len(kategorije) > 10 or len(kategorije) < 3:
                    sweetify.sweetalert(request, title="Unesite od 3 do 10 kategorija", icon="error")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                UserCategories.objects.filter(userID=user).delete()

                for k in kategorije:
                    cat = Category.objects.filter(pk=int(k)).filter(type=4)[0]
                    userCat = UserCategories(userID=user, categoryID=cat)
                    userCat.save()

                userP.editovanProfil = True

                user.save()
                emp.save()
                userP.save()

                return redirect('home')

    return redirect('profil')


def onama(request):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        if Company.objects.filter(userID=request.user).exists():
            usr = 'comp'
        else:
            usr = 'wrkr'

        userP = UserProfile.objects.get(userID=request.user)
        auth = True
        return render(request, 'onamanew.html', {'usr': usr, 'user': request.user, 'auth': auth, 'userP': userP, 'industries': None})
    else:
        auth = False
        industries = Category.objects.filter(type=0)
        return render(request, 'onamanew.html', {'usr': None, 'user': request.user, 'auth': auth, 'industries': industries})


def konsalting(request):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        if Company.objects.filter(userID=request.user).exists():
            usr = 'comp'
        else:
            usr = 'wrkr'

        user = request.user
        userP = UserProfile.objects.get(userID=user)
        return render(request, 'konsalting.html', {'usr': usr, 'user': user, 'userP':userP, 'auth': True, 'industries': None})
    else:
        industries = Category.objects.filter(type=0)
        return render(request, 'konsalting.html', {'usr': None, 'user': None, 'userP':None, 'auth': False, 'industries': industries})


def pretraga(request):

    auth = False

    if request.user.is_authenticated:
        auth = True

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    usr = None

    user = request.user
    userP = None

    if request.POST.get('pretragaTrigger', "False") == "True":
        grad = request.POST.get('gradovi', None)
        kategorija = request.POST.get('kategorije', None)
        kljucnaRijec = request.POST.get('kljucnaRijec', None)

        if Company.objects.filter(userID=user).exists():

            userComp = Company.objects.filter(userID=user)[0]
            if superUser(request.user):
                posts = Post.objects.all().exclude(expires_at__lte=datetime.now()).exclude(soft_delete=True)
            elif userComp.categoryID.name == "Finansijske":
                posts = Post.objects.all().filter(type=2).exclude(categoryID__name="Osiguravajuće").exclude(expires_at__lte=datetime.now()).exclude(soft_delete=True)
            elif userComp.categoryID.name == "Osiguravajuće":
                posts = Post.objects.all().filter(type=2).exclude(categoryID__name="Finansijske").exclude(expires_at__lte=datetime.now()).exclude(soft_delete=True)
            else:
                posts = Post.objects.all().filter(type=2).exclude(categoryID__name="Finansijske").exclude(categoryID__name="Osiguravajuće").exclude(expires_at__lte=datetime.now()).exclude(soft_delete=True)
        else:
            posts = Post.objects.filter(type=1).exclude(expires_at__lte=datetime.now()).exclude(soft_delete=True)

        if grad is not None:
            posts = posts.filter(location=grad)
        if kategorija is not None:
            ind = Category.objects.filter(name=kategorija)[0]
            posts = posts.filter(categoryID=ind)
        if kljucnaRijec is not "":
            posts = posts.filter(Q(title__contains=kljucnaRijec) | Q(content__contains=kljucnaRijec) | Q(categoryID__name__contains=kljucnaRijec))

    else:
        if Company.objects.filter(userID=user).exists():
            usr = 'comp'
            posts = Post.objects.all().filter(type=2).exclude(soft_delete=True)
        else:
            usr = 'wrkr'
            posts = Post.objects.all().filter(type=1).exclude(soft_delete=True)

    pretrazuje = request.POST.get('pretragaTrigger', "False")

    if superUser(request.user) and pretrazuje == "False":
        posts = Post.objects.all().exclude(expires_at__lte=datetime.now()).exclude(soft_delete=True)

    data = posts.exclude(expires_at__lte=datetime.now())
    counter = data.count()
    data = list(data)
    userP = UserProfile.objects.get(userID=user)
    gradovi = City.objects.all()
    cat = Category.objects.filter(type=1)
    users = User.objects.all()
    userPs = UserProfile.objects.all()
    btb = ["Ponuda", "Potražnja", "Partnerstvo"]
    return render(request, 'pretrazi.html',
                  {'usr': usr, 'iterRange': range(0, counter, 3), 'user': user, 'data': data, 'gradovi': gradovi, 'cat': cat, 'userP': userP, 'auth': auth, 'counter': counter, 'users': users, 'userPs': userPs, 'btb': btb})


def dashboard(request):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        if superUser(request.user):
            super = True
        else:
            super = False

        if Company.objects.filter(userID=request.user).exists():

            userP = UserProfile.objects.get(userID=request.user)
            aktPostovi = Post.objects.filter(userID=request.user).exclude(soft_delete=True).order_by('-created_at')
            inaktPostovi = Post.objects.filter(userID=request.user).exclude(soft_delete=False).order_by('-created_at')
            company = Company.objects.get(userID=request.user)

            rel1 = Post.objects.filter(type=2).filter(b2b_type=1).exclude(soft_delete=True).exclude(userID=request.user)
            rel2 = Post.objects.filter(type=2).filter(b2b_type=2).exclude(soft_delete=True).exclude(userID=request.user)
            rel3 = Post.objects.filter(type=2).filter(b2b_type=3).exclude(soft_delete=True).exclude(userID=request.user)

            relevantPosts = list(chain(rel1, rel2, rel3))

            paginator = Paginator(aktPostovi, 5)
            page = request.GET.get('pagea', 1)
            activePosts = paginator.page(page)
            rng = range(1, paginator.num_pages + 1)

            paginator2 = Paginator(inaktPostovi, 5)
            page2 = request.GET.get('pagez', 1)
            inactivePosts = paginator2.page(page2)
            rng2 = range(1, paginator2.num_pages + 1)

            return render(request, 'dashboard.html', {'usr': 'comp', 'super': super, 'user': request.user,
                                                      'userP': userP, 'auth': True, 'ind': None, 'activePosts': activePosts,
                                                      'inactivePosts': inactivePosts, 'relevantPosts': relevantPosts,
                                                      'page': int(page), 'rng': rng, 'page2': int(page2), 'rng2': rng2})
        else:
            return HttpResponseRedirect(request.META.get('HTTP_RENDERER', '/'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_RENDERER', '/'))


def anonimnaPretraga(request, id):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        if Company.objects.filter(userID=request.user).exists():
            usr = 'comp'
        else:
            usr = 'wrkr'

        auth = True
        userP = UserProfile.objects.get(userID=request.user)
    else:
        auth = False
        userP = None
        usr = None
    if id == '1':
        postovi = Post.objects.all().exclude(soft_delete=True).exclude(type=2).exclude(
            userID__first_name='Ziza').exclude(soft_delete=True)
        zizaPosts = Post.objects.filter(userID__first_name='Ziza').exclude(type=2).exclude(soft_delete=True)
    elif id == '2':
        postovi = Post.objects.all().exclude(soft_delete=True).exclude(type=1).exclude(
            userID__first_name='Ziza').exclude(soft_delete=True)
        zizaPosts = Post.objects.filter(userID__first_name='Ziza').exclude(type=1).exclude(soft_delete=True)
    else:
        return redirect('home')

    if request.POST.get('pretragaTrigger', "False") == "True":
        grad = request.POST.get('gradovi', None)
        kategorija = request.POST.get('kategorije', None)
        kljucnaRijec = request.POST.get('kljucnaRijec', None)

        if grad is not None:
            zizaPosts = zizaPosts.filter(location=grad)
            postovi = postovi.filter(location=grad)
        if kategorija is not None:
            ind = Category.objects.get(name=kategorija)
            zizaPosts = zizaPosts.filter(categoryID=ind)
            postovi = postovi.filter(categoryID=ind)
        if kljucnaRijec is not "":
            zizaPosts = zizaPosts.filter(Q(title__contains=kljucnaRijec) | Q(content__contains=kljucnaRijec))
            postovi = postovi.filter(Q(title__contains=kljucnaRijec) | Q(content__contains=kljucnaRijec))

    data = list(zizaPosts) + list(postovi)
    counter = len(data)
    #paginator = Paginator(data, 9)
    #page = request.GET.get('page', 1)
    #posts = paginator.page(page)
    #data = list(posts)
    number_pages = range(1,1)
    gradovi = City.objects.all()
    cat = Category.objects.filter(type=1)
    users = User.objects.all()
    userPs = UserProfile.objects.all()
    iterRange = range(0, counter, 3)
    btb = ["Ponuda", "Potražnja", "Partnerstvo"]
    return render(request, 'testPretraga.html',
                  {'data': data, 'gradovi': gradovi, 'cat': cat, 'auth': auth,
                   'counter': counter, 'users': users, 'btb': btb, 'userPs': userPs, 'iterRange': iterRange, 'userP': userP,
                   'usr': usr, 'number_pages': number_pages, 'page': int(1), 'id': id})


def firme(request):

    if request.user.is_authenticated:
        user = request.user
        userP = UserProfile.objects.get(userID=user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        if Company.objects.filter(userID=user).exists():
            usr = 'comp'
        else:
            usr = 'wrkr'

        kompanije = Company.objects.all()
        return render(request, 'firme.html', {'auth': True, 'usr': usr, 'userP': userP, 'user': user, 'kompanije': kompanije})
    else:
        usr = 'wrkr'

        kompanije = Company.objects.all()
        return render(request, 'firme.html', {'auth': False, 'usr': usr, 'userP': None, 'user': None, 'kompanije': kompanije})


def sifraMail(request, recipientMail):

    user = User.objects.get(email=recipientMail)
    tempSifra = get_random_string(length=10)
    current_site = get_current_site(request)

    mail_subject = "Obnovi lozinku"
    message = render_to_string('forgotPass.html', {
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'tempSifra': tempSifra,
        'domain': current_site.domain,
    })

    email = EmailMessage(
        mail_subject, message, to=[recipientMail]
    )

    email.send()


def forgotPassword(request):

    mail = request.POST.get('mailres', None)

    if mail is None:
        sweetify.sweetalert(request, title="Unesite svoju Email adresu", icon="error", timer=10000)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    elif User.objects.filter(email=mail).exists():
        sifraMail(request, mail)
        sweetify.sweetalert(request, title="Link za obnovu lozinke vam je poslan na email", icon="success", timer=10000)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        sweetify.sweetalert(request, title="Ne postoji korisnik sa ovom email adresom", icon="error", timer=10000)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def resetPass(request, uidb64, token, sifra):

    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.set_password(sifra)
        user.save()

        sweetify.sweetalert(request, title="Lozinka uspješno promijenjena", icon="success", timer=10000)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def csrf_failure(request, reason=""):

    if resolve(request.path_info).url_name == 'signin/':
        sweetify.sweetalert(request, title="Već ste prijavljeni", icon="error")
        return redirect('home')


def profilKorisnika(request, id, slug):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        user = User.objects.get(pk=id)

        slugified = slugify(user.first_name)

        if Company.objects.filter(userID=request.user).exists():
            usr = 'comp'
        else:
            usr = 'wrkr'

        if Company.objects.filter(userID=user).exists():
            company = Company.objects.get(userID=user)
            userP = UserProfile.objects.get(userID=user)
            postovi = Post.objects.filter(soft_delete=False).filter(userID=user)

            paginator = Paginator(postovi, 5)
            page = request.GET.get('page', 1)
            posts = paginator.page(page)
            rng = range(1, paginator.num_pages + 1)

            if slug == slugified:
                return render(request, 'ProfilKorisnika.html', {'usr': usr, 'auth': True, 'user': user, 'userP': userP,
                                                            'company': company, 'posts': posts, 'rng': rng, 'page': int(page)})
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            user = User.objects.get(pk=id)

            emp = Employee.objects.get(userID=user)
            vjestine = UserCategories.objects.filter(userID=user)

            return render(request, 'ProfilKorisnikaLP.html', {'userP': userP, 'emp': emp, 'vjestine': vjestine,
                                                              'auth': True, 'usr': 'wrkr', 'user': user})


def zizaKorisnika(request, id):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')
        usr = 'wrkr'
        user = User.objects.get(pk=id)
        if Company.objects.filter(userID=user).exists() and Company.objects.filter(userID=request.user).exists():
            usr = 'comp'
            userP = UserProfile.objects.get(userID=request.user)
            uProfil = UserProfile.objects.get(userID=user)
            activePosts = Post.objects.filter(userID=user).exclude(soft_delete=True).order_by('-created_at')
            inactivePosts = Post.objects.filter(userID=user).exclude(soft_delete=False).order_by('-created_at')
            company = Company.objects.get(userID=user)
            relevantPosts = Post.objects.filter(categoryID=company.categoryID)
            return render(request, 'zizaKorisnika.html',
                          {'usr': usr, 'uProfil': uProfil, 'user': request.user, 'userP': userP, 'auth': True, 'ind': None,
                           'activepPosts': activePosts,'inactivePosts': inactivePosts, 'relevantPosts': relevantPosts})
    sweetify.sweetalert(request, title="Akcija nije dozvoljena", icon="error")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def postpone(function):

    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

@postpone
def contactAll(request):

    if not superUser(request.user):
        return redirect('home')

    subject = request.POST['subject']
    sadrzaj = request.POST['message']

    mail_subject = subject
    message = sadrzaj

    users = User.objects.all()

    for u in users:

        email = EmailMessage(
            mail_subject, message, to=[u.email]
        )

        email.send()

    sweetify.sweetalert(request, title="Mail poslan", icon="success")
    return redirect('home')


def mojaKarijera(request):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        user = request.user

        categories = Category.objects.filter(usercategories__userID=user)

        activePosts = Post.objects.filter(workersposts__userID=user).exclude(soft_delete=True)
        inactivePosts = Post.objects.filter(workersposts__userID=user).exclude(soft_delete=False)
        relevantPosts = Post.objects.filter(categoryID__in=categories)

        return render(request, 'mojaKarijera.html', {'user': user, 'userP': userP, 'activePosts': activePosts,
                                                     'inactivePosts': inactivePosts, 'auth': True, 'ind': None,
                                                     'relevantPosts': relevantPosts, 'usr': 'wrkr'})

    return redirect('home')


def mailSvima(request):

    if superUser(request.user):
        user = request.user
        userP = UserProfile.objects.get(userID=user)
        return render(request, 'conatctAll.html', {'user': user, 'userP': userP})

##novo


def konsalting_detailed(request, slug):
    return render(request, slug+'.html')


def testclanovi(request):
    usr = 'wrkr'
    return render(request, 'testclanovi.html', {'usr': usr, 'userP': None, 'user': None})


def korisnik(request):

    return render(request, 'korisnik.html')


def CVs(request):

    userP = UserProfile.objects.get(userID=request.user)

    if not userP.editovanProfil:
        sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
        return redirect('editprofil')

    employees = Employee.objects.all()

    userPrs = UserProfile.objects.filter(userID__employee__in=employees)

    paginator = Paginator(userPrs, 10)
    page = request.GET.get('page', 1)
    rng = range(1, paginator.num_pages + 1)
    userPs = paginator.page(page)

    return render(request, 'CVs.html', {'employees': employees, 'userPs': userPs, 'auth': True, 'userP': userP,
                                        'rng': rng, 'page': int(page)})


def pozovi(request, id, sender):

    if request.user.is_authenticated:

        if request.method == 'POST':

            sweetify.sweetalert(request, title="Korisnik je obaviješten da ga zelite kontaktirati", icon="success")
            user = User.objects.get(pk=id)

            sender = User.objects.get(pk=sender)

            title = "Kontakt"
            message = render_to_string('pozovi.html', {'sender': sender})

            email = EmailMessage(title, message, to=[user.email])

            email.send()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
