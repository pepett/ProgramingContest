from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from lib.utils import Utils

# Create your views here.
def top( request ):
    #例ここから
    tmp = Utils.sharp( "unti unti #aaaa \n un#ti #bbb jsflkdsj" )
    for counter in range( len( tmp ) ):
        print( tmp[ counter ] )
    #例ここまで
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
        lz_uri = 'spotify:artist:3wvCMqwyJachksGLF0kjMJ'
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='811426a7bad2420c98d9f2d03a88141d',client_secret='62e88e7c02754132ab2af5f4078543fc',))
        results = spotify.artist_top_tracks(lz_uri)
        final_result=results['tracks']
        for tracks in final_result:
            return render(request,'cwm/index.html',{"results":final_result})

def music( request ):
    return render( request, 'cwm/music.html' )

def user( request ):
    return render( request, 'cwm/user.html' )

def search( request ):
    return render( request, 'cwm/search.html' )