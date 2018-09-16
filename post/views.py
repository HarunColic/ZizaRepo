from django.shortcuts import render, redirect
from post.models import Post, Industry, Category, PostCategories
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from account.models import Company, Employee, UserProfile
from location.models import City
import sweetify
from django.http import HttpResponseRedirect


def newpost(request):

    if Company.objects.filter(userID=request.user):

        data = Industry.objects.all()
        categories = Category.objects.all()
        userP = UserProfile.objects.get(userID=request.user)
        return render(request, 'newpost.html', {'data': data, 'cat': categories, 'userP': userP, 'user': request.user})
    else:
        return redirect('home')


def newpotraznja(request):

    if Company.objects.filter(userID=request.user):

        categories = Category.objects.all()
        industries = Industry.objects.all()
        comp = Company.objects.get(userID=request.user)
        userP = UserProfile.objects.get(userID=request.user)

        return render(request, 'dodajPotraznju.html', {'ind': industries, 'cat': categories, 'comp': comp, 'user': request.user, 'userP': userP})
    else:
        return redirect('home')


def createpost(request):

    if request.method == 'POST':

        if request.POST['type'] == "1":

            title = request.POST['naslov']
            category = request.POST['category']
            expiration = request.POST['expiration']
            lokacija = request.POST['lokacija']
            pozicija = request.POST['pozicija']
            godineIskustva = request.POST['godineIskustva']
            strucnasprema = request.POST['strucnasprema']
            email = request.POST['email']
            brojTel = request.POST['brojTel']
            opis = request.POST['opis']
            type = request.POST['type']

            cat = Category.objects.get(name=category)

            if City.objects.all().filter(name=lokacija).exists():
                city = City.objects.get(name=lokacija)
            else:
                city = City(name=lokacija)
                city.save()

            post = Post(userID=request.user, title=title, region="BiH", location=city.name, position=pozicija, type=type, specialty=strucnasprema, experience=godineIskustva, contact_email=email, contact_phone=brojTel, content=opis, expires_at=datetime.now()+timedelta(days=int(expiration)))
            post.save()

            postcat = PostCategories(postID=post, categoryID=cat)

            postcat.save()

            sweetify.success(request, title="Uspješno kreiran oglas", text="", icon="success", timer=8000)

            return redirect('newpost')
        else:

            type = request.POST['type']
            btobtype = request.POST['b2btype']
            category = request.POST['category']
            kanton = request.POST['kanton']
            trajanje = request.POST['expiration']
            email = request.POST['email']
            brojTel = request.POST['brojTel']
            opis = request.POST['opis']


            post = Post(userID=request.user, type=int(type), b2b_type=int(btobtype), region=kanton, expires_at=datetime.now()+timedelta(days=int(trajanje)), contact_email=email, contact_phone=brojTel, content=opis)

            post.save()

            cat = Category.objects.get(name=category)

            postCategories = PostCategories(postID=post, categoryID=cat)
            postCategories.save()

            sweetify.success(request, title="Uspješno kreiran oglas", icon="success", timer=8000)

            return redirect('newpotraznja')

    return redirect('home')


def showpost(request, id):
    post = Post.objects.get(pk=id)
    userP = UserProfile.objects.get(userID=post.userID)

    if post.soft_delete:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    elif post.is_past_due:
        post.soft_delete = True
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return render(request, 'oglas.html', {'post': post, 'userP': userP})



