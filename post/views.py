from django.shortcuts import render, redirect
from post.models import Post, Industry, Category, PostCategories
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from account.models import Company, Employee


def newpost(request):

    if Company.objects.filter(userID=request.user):

        data = Industry.objects.all()
        categories = Category.objects.all()
        return render(request, 'newpost.html', {'data': data, 'cat': categories})
    else:
        return redirect('home')


def newpotraznja(request):

    if Company.objects.filter(userID=request.user):

        categories = Category.objects.all()
        industries = Industry.objects.all()
        return render(request, 'dodajPotraznju.html', {'ind': industries, 'cat': categories})
    else:
        return redirect('home')


def createpost(request):

    if request.method == 'POST':

        if request.POST['type'] == "1":

            title = request.POST['naslov']
            category = request.POST['category']
            industry = request.POST['industry']
            expiration = request.POST['expiration']
            lokacija = request.POST['lokacija']
            pozicija = request.POST['pozicija']
            godineIskustva = request.POST['godineIskustva']
            strucnasprema = request.POST['strucnasprema']
            email = request.POST['email']
            brojTel = request.POST['brojTel']
            opis = request.POST['opis']
            type = request.POST['type']

            indust = Industry.objects.get(name=industry)
            cat = Category.objects.get(name=category)

            post = Post(userID=request.user, title=title, industryID=indust, region="BiH", location=lokacija, position=pozicija, type=type, specialty=strucnasprema, experience=godineIskustva, contact_email=email, contact_phone=brojTel, content=opis, expires_at=datetime.now()+timedelta(days=int(expiration)))
            post.save()

            postcat = PostCategories(postID=post, categoryID=cat)

            postcat.save()

            return redirect('newpost')
        else:

            type = request.POST['type']
            btobtype = request.POST['b2btype']
            industry = request.POST['Industry']
            category = request.POST['category']
            kanton = request.POST['kanton']
            trajanje = request.POST['expiration']
            email = request.POST['email']
            brojTel = request.POST['brojTel']
            opis = request.POST['opis']

            ind = Industry.objects.get(name=industry)

            post = Post(userID=request.user, type=int(type), b2b_type=int(btobtype), industryID=ind, region=kanton, expires_at=datetime.now()+timedelta(days=int(trajanje)), contact_email=email, contact_phone=brojTel, content=opis)

            post.save()

            cat = Category.objects.get(name=category)

            postCategories = PostCategories(postID=post, categoryID=cat)
            postCategories.save()

            return redirect('newpotraznja')

    return redirect('home')


def showpost(request, id):
    post = Post.objects.get(pk=id)

    return render(request, 'oglas.html', {'post': post})
