"""Ziza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from account import views as AC_Views
from post import views as P_Views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url('admin/', admin.site.urls),
    url('^$', AC_Views.home, name='home'),
    url('^home$', AC_Views.home, name='home'),
    url('register/', AC_Views.register, name='register'),
    url('signin/', AC_Views.signin, name='signin'),
    url('signout/', AC_Views.signout, name='signout'),
    url('newpost/', P_Views.newpost, name='newpost'),
    url('createpost/', P_Views.createpost, name='createpost'),
    url('newpotraznja/', P_Views.newpotraznja, name='newpotraznja'),
    url(r'^showpost/(?P<id>[0-9]+)/', P_Views.showpost, name='showpost'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        AC_Views.activate, name='activate'),
    url('onama/', AC_Views.onama, name='onama'),
    url('^profil/', AC_Views.profil, name='profil'),
    url('editprofil/', AC_Views.editprofil, name='editprofil'),
    url('^submitchange/', AC_Views.submitchange, name='submitchange'),
    url('^pretraga/', AC_Views.pretraga, name='pretraga'),
    url('^konsalting/', AC_Views.konsalting, name='konsalting'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
