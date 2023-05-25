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
        def truncate_string(text, max_length):
            if len(text) <= max_length:
                return text
            else:
                return text[:max_length] + "..."

        max_length = 15

        lz_uri = 'spotify:artist:3wvCMqwyJachksGLF0kjMJ'
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='811426a7bad2420c98d9f2d03a88141d',client_secret='62e88e7c02754132ab2af5f4078543fc',))
        results = spotify.artist_top_tracks(lz_uri)
        final_result=results['tracks']

        lz_uri2 = 'spotify:artist:1snhtMLeb2DYoMOcVbb8iB'
        spotify2 = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='811426a7bad2420c98d9f2d03a88141d',client_secret='62e88e7c02754132ab2af5f4078543fc',))
        results2 = spotify2.artist_top_tracks(lz_uri2)
        final_result2=results2['tracks']

        lz_uri3 = 'spotify:artist:5Vo1hnCRmCM6M4thZCInCj'
        spotify3 = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='811426a7bad2420c98d9f2d03a88141d',client_secret='62e88e7c02754132ab2af5f4078543fc',))
        results3 = spotify3.artist_top_tracks(lz_uri3)
        final_result3=results3['tracks']

        j = 0
        for i in final_result:
            final_result[j]['name'] = truncate_string(i['name'],max_length)
            final_result[j]['artists'][0]['name'] = truncate_string(i['artists'][0]['name'],max_length)
            j = j + 1

        j = 0
        for i in final_result2:
            final_result2[j]['name'] = truncate_string(i['name'],max_length)
            final_result2[j]['artists'][0]['name'] = truncate_string(i['artists'][0]['name'],max_length)
#            print( i[ 'id' ] )//これをデータベースに入れる
            j = j + 1

        j = 0
        for i in final_result3:
            final_result3[j]['name'] = truncate_string(i['name'],max_length)
            final_result3[j]['artists'][0]['name'] = truncate_string(i['artists'][0]['name'],max_length)
            j = j + 1

        for tracks in final_result:
            return render(request,'cwm/index.html',{"results":final_result,"results2":final_result2,"results3":final_result3})

def music( request ):
    return render( request, 'cwm/music.html' )

def user( request ):
    return render( request, 'cwm/user.html' )

def search( request ):
    return render( request, 'cwm/search.html' )