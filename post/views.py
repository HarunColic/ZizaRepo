from django.shortcuts import render, redirect
from post.models import Post, Category, PostCategories
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from account.models import Company, Employee, UserProfile
from location.models import City
import sweetify
from django.http import HttpResponseRedirect
from account import views
from account.views import validation


def newpost(request):
    if views.soon.soon:
        return redirect('/')
    else:
        if Company.objects.filter(userID=request.user):

            categories = Category.objects.all()
            userP = UserProfile.objects.get(userID=request.user)
            return render(request, 'newpost.html', {'cat': categories, 'userP': userP, 'user': request.user})
        else:
            return redirect('home')


def newpotraznja(request):
    if views.soon.soon:
        return redirect('/')
    else:
        if Company.objects.filter(userID=request.user):

            categories = Category.objects.all()
            comp = Company.objects.get(userID=request.user)
            userP = UserProfile.objects.get(userID=request.user)

            return render(request, 'dodajPotraznju.html', {'cat': categories, 'comp': comp, 'user': request.user, 'userP': userP})
        else:
            return redirect('home')


def createpost(request):
    if views.soon.soon:
        return redirect('/')
    else:
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

                args = [title, category, expiration, lokacija, pozicija, godineIskustva, strucnasprema, email, brojTel, opis, type]

                if not validation(request, args):
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                cat = Category.objects.get(name=category)

                if City.objects.all().filter(name=lokacija).exists():
                    city = City.objects.get(name=lokacija)
                else:
                    city = City(name=lokacija)
                    city.save()

                post = Post(userID=request.user, categoryID=cat, title=title, region="BiH", location=city.name, position=pozicija, type=type, specialty=strucnasprema, experience=godineIskustva, contact_email=email, contact_phone=brojTel, content=opis, expires_at=datetime.now()+timedelta(days=int(expiration)))
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

                post = Post(position=position, title=title, userID=request.user, categoryID=cat, type=int(type), b2b_type=int(btobtype), region=kanton, expires_at=datetime.now()+timedelta(days=int(trajanje)), contact_email=email, contact_phone=brojTel, content=opis)

                post.save()

                postCategories = PostCategories(postID=post, categoryID=cat)
                postCategories.save()

                sweetify.success(request, title="Uspješno kreiran oglas", icon="success", timer=8000)

                return redirect('newpotraznja')

        return redirect('home')


def showpost(request, id):
    if views.soon.soon:
        return redirect('/')
    else:
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
            return render(request, 'oglas.html', {'post': post, 'userP': userP, 'b2b': b2b})

def bankUsluge(request):

    if views.soon.soon:
        return redirect('/')
    else:
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