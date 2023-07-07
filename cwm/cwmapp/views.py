import os
import re
import json
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from lib.spotify_conect import SPOTIFY
from lib.utils import Utils
from cwmapp.models import User, Comment, HistoryList, LikeList, Music, Star

from .forms import CommentForm, UploadImageForm, UsernameForm, RegisterForm, CustomUser#, LoginForm

# Create your views here.

#仮ログイン
IsLogin = True
UserData = User.objects.filter( user_mail = 'k228021@kccollege.ac.jp' )

def top( request ):
    #例ここから 
    #tmp = Utils.sharp( "unti unti #aaaa \n un#ti #bbb jsflkdsj" )
    #for counter in range( len( tmp ) ):
    #    print( tmp[ counter ] )
    #例ここまで
    if request.user.is_authenticated:
        print( request.user.last_login )
    return render( request, 'cwm/top.html' )
def Login( request ):
    if request.POST:
        email = request.POST[ 'email' ]
        password = request.POST[ 'password' ]
        user = authenticate( request, email=email, password=password )
        if user is not None:
            login( request, user )
            return redirect( 'index' )
        else:
            pass
    return render( request, 'cwm/login.html' )

def Logout( request ):
    if request.user.is_authenticated:
        logout( request )
        return redirect( '/' )
    else:
        print( 'error' )

def register( request ):
    if request.POST:
        img = Utils.CreateUserImage(request.POST['username'])
        register_form = RegisterForm( request.POST)
        if register_form.is_valid():
            reg = register_form.save()
            print(reg)
            print(img)
            reg.set_password( reg.password )
            reg.image = img
            reg.save()
            content = {
                'register_form': register_form
            }
            return redirect( 'Login' )
        else:
            content = {
                'register_form': register_form
            }
    else:
        content = {
            'register_form': None
        }
    return render( request, 'cwm/register.html', content )

def setting( request ):
    
    if not request.user.is_authenticated:
        return redirect(Login)
    
    User = CustomUser.objects.filter( email = request.user.email )
    Likeresult = []
    Historyresult = []
    content = {
        "results":Likeresult,
        "results2":Historyresult,
        "upload_form":UploadImageForm(),
        "data":User,
        "username_form":UsernameForm(),
        "id":None
    }
    if (request.method == 'POST'):
        NewUsername = request.POST['NewUsername']
        print('NewUsername1'+NewUsername)
        if (request.FILES):
            if NewUsername:
                User.update(username = NewUsername)
                UpdateFileName = NewUsername+os.path.splitext(request.FILES['image'].name)[1]
                print('UpdateFileName1'+UpdateFileName)
            else:
                UpdateFileName = request.user.username+os.path.splitext(request.FILES['image'].name)[1]
                print('UpdateFileName2'+UpdateFileName)
            request.FILES['image'].name = UpdateFileName
            User[0].image.delete()
            image = UploadImageForm(request.POST,request.FILES)
            image.save()
            User.update(image = 'images/'+UpdateFileName)

        elif (request.POST['NewUsername']):
            UpdateFileName = NewUsername+os.path.splitext(User[0].image.name)[1]
            print('UpdateFileName3'+UpdateFileName)
            User.update(username = NewUsername)

    MusHistory = HistoryList.objects.filter(history_user_mail = request.user.email)
    MusLiked = LikeList.objects.filter(like_user_mail = request.user.email)

    max_length = 13

    for i in range(MusHistory.count()):
        for j in range(MusHistory.count())[i + 1:]:
            if MusHistory[i].history_music_id == MusHistory[j].history_music_id:
                print('MusHistory:'+str(i)+':'+str(j))
                print('history_music_id:'+MusHistory[i].history_music_id+':'+MusHistory[j].history_music_id)
                MusHistory[i].delete()
                break

    for i in range(MusLiked.count()):
        for j in range(MusLiked.count())[i + 1:]:
            if MusLiked[i].like_music_id == MusLiked[j].like_music_id:
                print('MusLiked:'+str(i)+':'+str(j))
                print('like_music_id:'+MusLiked[i].like_music_id+':'+MusLiked[j].like_music_id)
                MusLiked[i].delete()

    for i in MusHistory:
        x = SPOTIFY.track(i.history_music_id)
        Historyresult.append(x)

    Historyresult.reverse()

    for i in MusLiked:
        x = SPOTIFY.track(i.like_music_id)
        Likeresult.append(x)

    Likeresult.reverse()


    j = 0
    for i in Likeresult:
        Likeresult[j]['name'] = Utils.truncate_string(i['name'],max_length)
        Likeresult[j]['artists'][0]['name'] = Utils.truncate_string(i['artists'][0]['name'],max_length)
        j = j + 1

    j = 0
    for i in Historyresult:
        Historyresult[j]['name'] = Utils.truncate_string(i['name'],max_length)
        Historyresult[j]['artists'][0]['name'] = Utils.truncate_string(i['artists'][0]['name'],max_length)
        j = j + 1

    content['results'] = Likeresult[:30]
    content['results2'] = Historyresult[:30]
    content['user'] = User
    return render(request,'cwm/setting.html',content)


def result( request ):
    if not request.GET[ 'search-music' ]:
        return redirect( 'search' )
    res = Comment.objects.filter( comment_text__regex = request.GET[ 'search-music' ] )
    ctracks = []
    for i in res:
        t = {
            'c_music': SPOTIFY.track( i.comment_music_id, market=None ),
            'c_text': i.comment_text
        }
        ctracks.append( t )

    li = 10
    results_track = SPOTIFY.search( request.GET['search-music'], limit=li, offset=0, type='track,album,artist', market=None )
    for i in range( li ):
        pass
        #results_track[ 'tracks' ][ 'items' ][ i ][ 'name' ] = Utils.truncate_string(results_track[ 'tracks' ][ 'items' ][ i ][ 'name' ], 9)
        #results_track[ 'albums' ][ 'items' ][ i ][ 'name' ] = Utils.truncate_string(results_track[ 'albums' ][ 'items' ][ i ][ 'name' ], 9)
        #results_track[ 'artists' ][ 'items' ][ i ][ 'name' ] = Utils.truncate_string(results_track[ 'artists' ][ 'items' ][ i ][ 'name' ], 9)
    #if results_track[ 'artists' ][ 'items' ][ i ][ 'images' ][ 0 ][ 'url' ] == None:
    #    print( 'aa' )
    #    results_track[ 'artists' ][ 'items' ][ i ][ 'images' ][ 0 ][ 'url' ] = "{% static 'img/tmp/karee.jpg' %}"
    ret = {
        'results_track': results_track,
        'word': request.GET[ 'search-music' ],
        'hitcmt': res,
        'c_tracks': ctracks,
    }
    return render( request, 'cwm/result.html', ret  )

def index( request ):

    final_result = []
    final_result2 = []
    final_result3 = []
    User = False

    content = {
        "results":final_result,
        "results2":final_result2,
        "results3":final_result3,
        "data":User
    }
    
    if request.user.is_authenticated:
        User = CustomUser.objects.filter( email = request.user.email )
        content[ 'data' ] = User

    max_length = 13
    Playlist_uri = 'spotify:playlist:37i9dQZEVXbKXQ4mDTEBXq'
    
    results = SPOTIFY.playlist_tracks(Playlist_uri)['items']
    final_result = results[:10]

    lz_uri2 = 'spotify:artist:1snhtMLeb2DYoMOcVbb8iB'
    results2 = SPOTIFY.artist_top_tracks(lz_uri2)
    final_result2=results2['tracks']

    lz_uri3 = 'spotify:artist:5Vo1hnCRmCM6M4thZCInCj'
    results3 = SPOTIFY.artist_top_tracks(lz_uri3)
    final_result3=results3['tracks']

    #j = 0
    #for i in final_result:
    #    final_result[j]['track']['name'] = Utils.truncate_string(i['track']['name'],max_length)
    #    final_result[j]['track']['artists'][0]['name'] = Utils.truncate_string(i['track']['artists'][0]['name'],max_length)
    #    j = j + 1

    #j = 0
    #for i in final_result2:
    #    final_result2[j]['name'] = Utils.truncate_string(i['name'],max_length)
    #    final_result2[j]['artists'][0]['name'] = Utils.truncate_string(i['artists'][0]['name'],max_length)
#            print( i[ 'id' ] )//これをデータベースに入れる
    #    j = j + 1

    #j = 0
    #for i in final_result3:
    #    final_result3[j]['name'] = Utils.truncate_string(i['name'],max_length)
    #    final_result3[j]['artists'][0]['name'] = Utils.truncate_string(i['artists'][0]['name'],max_length)
    #    j = j + 1

    content['results'] = final_result
    content['results2'] = final_result2
    content['results3'] = final_result3

    return render(request,'cwm/index.html',content)

def create( request, idn ):
    if request.method == 'POST':
        c = Comment( comment_user_mail=request.user.email, comment_music_id=idn, comment_good=0, comment_text=request.POST[ 'comment_text' ] )
        c.save()
    return redirect( 'mus', idn )

def delete( request, idn, cid ):
    if request.method == 'POST':
        d = Comment.objects.get( comment_id = cid )
        d.delete()
    return redirect( 'mus', idn )

def edit( request, idn, cid ):
    if request.method == 'POST':
        e = Comment.objects.get( comment_id = cid )
        e.comment_text = request.POST[ 'edit_content' ]
        e.save()
    return redirect( 'mus', idn )

def music( request, idn ):
    ave_star = 0
    user_star = 0
    if Star.objects.filter( star_music_id = idn ).exists():
        for i in range( Star.objects.filter( star_music_id = idn ).count() ):
            ave_star += Star.objects.filter( star_music_id = idn )[ i ].star_num
        ave_star /= Star.objects.filter( star_music_id = idn ).count()
        ave_star = Utils.round( ave_star )
    if request.user.is_authenticated:
        if Star.objects.filter( star_user_mail = request.user.email, star_music_id = idn ).exists():
            user_star = Star.objects.get( star_user_mail = request.user.email, star_music_id = idn ).star_num
    
    track_result = SPOTIFY.track( idn, market=None )
    comments = []
    tags = []
    users = []
    form = CommentForm()
    mdl = []
    results = []
    content = {
        'track_result': track_result,#曲のトラック
        'comments': comments,#コメントのテーブルのレコード
        'tags': tags,#タグ
        'users': users,#
        'form': form,#コメント投稿用のフォーム
        #'db': UserData[ 0 ],#ログイン中のユーザ情報( 仮 )
        'model': mdl,
        'is_comment': False,
        'ave_star': ave_star,
        'user_star': user_star,
    }

    if request.user.is_authenticated:
        User = CustomUser.objects.filter( email = request.user.email )
        content[ 'data' ] = User
        MusHistory = HistoryList(history_user_mail = request.user.email,history_music_id = idn)
        MusHistory.save()

    if Comment.objects.filter( comment_music_id=idn ).exists():
        content[ 'is_comment' ] = True
        comments = Comment.objects.filter( comment_music_id=idn )
        for i in range( comments.count() ):
            users.append( CustomUser.objects.get( email=comments[ i ].comment_user_mail ) )#一つしかとってきてない
            tags.extend( Utils.sharp( comments[ i ].comment_text ) )
            tmp = {
                'user_name': users[ i ].username,
                'user_mail': users[ i ].email,
                'user_image': users[ i ].image,
                'comment_id': comments[ i ].comment_id,
                'comment_good': comments[ i ].comment_good,
                'comment_text': comments[ i ].comment_text,
                'comment_posted': comments[ i ].comment_posted,
                'result': results
            }
            mdl.append( tmp )
        
        tags = Utils.del_duplicate( tags, False )
        content[ 'tags' ] = tags
        content[ 'comments' ] = comments
        content[ 'users' ] = users
    return render( request, 'cwm/music.html', content )

def user( request ):
    db = User.objects.all()
    data = {
        'db': db,
    }
    return render( request, 'cwm/user.html', data )

def search( request ):
    #if len( request.GET[ 'search-music' ] ) != 0:
    return render( request, 'cwm/search.html')

def artist( request, id ):

    artist_result = []
    result = []
    artist_album = []
    related_artist = []
    User = False

    content = {
        'artist': artist_result,
        'results': result,
        'artist_album': artist_album,
        'related_artist': related_artist,
        'data': User
    }
    if request.user.is_authenticated:
        User = CustomUser.objects.filter( email = request.user.email )
        content[ 'data' ] = User

    max_length = [13,21]
    artist_result = SPOTIFY.artist( id )
    related_artist = SPOTIFY.artist_related_artists(id)
    related_result = related_artist['artists']
    artist_track = SPOTIFY.artist_top_tracks( id, country='JP' )
    result=artist_track['tracks']
    artist_album = SPOTIFY.artist_albums(id, album_type=None, country='JP', limit=50, offset=0)

    #j = 0
    #for i in result:
    #    result[j]['name'] = Utils.truncate_string(i['name'],max_length[0])
    #    result[j]['artists'][0]['name'] = Utils.truncate_string(i['artists'][0]['name'],max_length[0])
    #    j = j + 1

    j = 0
    for i in related_result:
        related_result[j]['name'] = Utils.truncate_string(i['name'],max_length[1])
        j = j + 1

    content[ 'artist' ] = artist_result
    content[ 'results' ] = result
    content[ 'artist_album' ] = artist_album
    content[ 'related_artist' ] = related_result

    return render( request, 'cwm/artist.html', content )

def album( request, id ):

    User = False

        
    if request.user.is_authenticated:
        User = CustomUser.objects.filter( email = request.user.email )

    albums = SPOTIFY.albums( [ id ], market=None )

    content = {
        'album_desc': albums[ 'albums' ][ 0 ],
        'album_tracks': albums[ 'albums' ][ 0 ][ 'tracks' ][ 'items' ],
        'data':User
    }
    return render( request, 'cwm/album.html', content )

def star( request, idn ):#非同期時に行う処理
    if request.POST:
        data = json.loads( request.POST[ 'star_n' ] )
        ave_star = 0
        user_star = 0

        if request.user.is_authenticated:
            #g_s = None
            if Star.objects.filter( star_user_mail = request.user.email, star_music_id = idn ).exists():
                g_s = Star.objects.get( star_user_mail = request.user.email, star_music_id = idn )
                st = data[ 'number' ] + 1
                g_s.star_num = st
                g_s.save()
            else:
                st = data[ 'number' ] + 1
                g_s = Star( star_user_mail = request.user.email, star_music_id = idn, star_num = st )
                g_s.save()
            user_star = g_s.star_num
        if Star.objects.filter( star_music_id = idn ).exists():
            for i in range( Star.objects.filter( star_music_id = idn ).count() ):
                ave_star += Star.objects.filter( star_music_id = idn )[ i ].star_num
            ave_star /= Star.objects.filter( star_music_id = idn ).count()
            ave_star = Utils.round( ave_star )
        content = {
            'ave_star': ave_star,
            'user_star': user_star,
        }
    return JsonResponse( content )