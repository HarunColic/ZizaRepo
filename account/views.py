from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from account.models import Company, Employee, UserProfile
from location.models import City
from post.models import Industry, Category
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from post.models import Post
from post.models import UserCategories, PostCategories


def home(request):

    if request.user.is_authenticated:

        user = request.user
        posts = Post.objects.all().filter(type=1)
        data = posts
        gradovi = City.objects.all()
        cat = Category.objects.all()
        counter = posts.count()
        return render(request, 'logiran.html', {'user': user, 'data': data, 'counter': counter, 'gradovi': gradovi, 'cat': cat})
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
            city = City()
            industry = Industry()

            city.name = request.POST['City']
            city.clean()
            city.name.lower()
            city.name.capitalize()

            if City.objects.filter(name=city.name).exists():
                city = City.objects.get(name=city.name)
            else:
                city.save()

            industry.name = request.POST['Industry']
            industry.clean()
            industry.name.lower()
            industry.name.capitalize()

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
