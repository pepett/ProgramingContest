from django.shortcuts import render

# Create your views here.
def top( request ):
    return render( request, 'cwm/top.html' )

def login( request ):
    return render( request, 'cwm/login.html' )

def register( request ):
    return render( request, 'cwm/register.html' )

def setting( request ):
    return render( request, 'cwm/setting.html' )

def result( request ):
    return render( request, 'cwm/result.html' )

def index( request ):
    return render( request, 'cwm/index.html' )

def music( request ):
    return render( request, 'cwm/music.html' )

def user( request ):
    return render( request, 'cwm/user.html' )

def search( request ):
    return render( request, 'cwm/search.html' )