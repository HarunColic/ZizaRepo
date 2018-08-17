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
                user.clean()
                user.save()

                emp = Employee(userID=user)
                emp.save()

                userP = UserProfile(userID=user)
                userP.save()

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

            return redirect('home')

    return redirect('home')


def signin(request):

    if request.method == 'POST':

        mail = request.POST['mail']
        password = request.POST['pswd']

        user = User.objects.get(email=mail)

        if user.check_password(password):
            login(request, user)

    return redirect('home')


def signout(request):

    logout(request)
    return redirect('home')
