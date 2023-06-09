"""
URL configuration for cwm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from cwmapp.views import top, Login, register, setting, result, index, music, user, search, artist, album, create, delete, edit, Logout, star, view_reply, create_reply, changepassword

app_name = 'cwm'

urlpatterns = [
    path('admin/', admin.site.urls),
    path( "", top ,name="top"),
    path( "login/", Login, name="Login"),
    path( "logout/", Logout, name="Logout" ),
    path( "register/", register ,name="register"),
    path( "setting/", setting ,name="setting"),
    path( "result/", result, name="result" ),
    path( "index/", index, name="index"),
    path( "create/<slug:idn>", create, name="create" ),
    path( "delete/<slug:idn>/<int:cid>", delete, name="delete" ),
    path( "edit/<slug:idn>/<int:cid>", edit, name="edit" ),
    path( "star/<slug:idn>", star, name="star" ),
    path( "view_reply/<slug:idn>", view_reply, name="view_reply" ),
    path( "create_reply/<slug:idn>/<int:cid>", create_reply, name="create_reply" ),
    path( "music/<slug:idn>", music, name="mus" ),
    path( "user/", user ),
    path( "search/", search, name="search" ),
    path( "artist/<slug:id>", artist, name="artist" ),
    path( "album/<slug:id>", album, name="album" ),
    path( "changepassword/", changepassword, name="changepassword" ),
]

#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)