import os
import re
from django.shortcuts import render
from django.shortcuts import redirect
from lib.spotify_conect import SPOTIFY
from lib.utils import Utils
from cwmapp.models import User, Comment, HistoryList, LikeList

from .forms import CommentForm, UploadImageForm, UsernameForm

# Create your views here.

#仮ログイン
IsLogin = True
UserData = User.objects.filter( user_mail = 'k228016@kccollege.ac.jp' )

def top( request ):
    #例ここから 
    #tmp = Utils.sharp( "unti unti #aaaa \n un#ti #bbb jsflkdsj" )
    #for counter in range( len( tmp ) ):
    #    print( tmp[ counter ] )
    #例ここまで
    return render( request, 'cwm/top.html' )
def login( request ):
    return render( request, 'cwm/login.html' )

def register( request ):
    return render( request, 'cwm/register.html' )

def setting( request ):

    if IsLogin == False:#ログインしていなければログインページにリダイレクト
        return redirect(login)
    
    Likeresult = []
    Historyresult = []
    content = {
        "results":Likeresult,
        "results2":Historyresult,
        "IsLogin":IsLogin,
        "data":UserData,
        "upload_form":UploadImageForm(),
        "username_form":UsernameForm(),
        "id":None
    }
    if (request.method == 'POST'):
        NewUsername = request.POST['NewUsername']
        if (request.FILES):
            UpdateFileName = UserData[0].user_name+os.path.splitext(request.FILES['image'].name)[1]
            if NewUsername:
                UpdateFileName = NewUsername+os.path.splitext(request.FILES['image'].name)[1]
            request.FILES['image'].name = UpdateFileName
            image = UploadImageForm(request.POST,request.FILES)
            print(str(request.FILES['image'].name))
            print(os.path.splitext(request.FILES['image'].name)[1])
            UserData[0].user_image.delete()
            if image.is_valid():
                image.save()
                User.objects.filter( user_mail = UserData[0].user_mail ).update(user_image = 'images/'+UpdateFileName)
                if NewUsername:
                    User.objects.filter( user_mail = UserData[0].user_mail ).update(user_name = NewUsername)

    MusHistory = HistoryList.objects.filter(history_user_mail = UserData[0].user_mail)
    MusLiked = LikeList.objects.filter(like_user_mail = UserData[0].user_mail)

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
        results_track[ 'tracks' ][ 'items' ][ i ][ 'name' ] = Utils.truncate_string(results_track[ 'tracks' ][ 'items' ][ i ][ 'name' ], 9)
        results_track[ 'albums' ][ 'items' ][ i ][ 'name' ] = Utils.truncate_string(results_track[ 'albums' ][ 'items' ][ i ][ 'name' ], 9)
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

    j = 0
    for i in final_result:
        final_result[j]['track']['name'] = Utils.truncate_string(i['track']['name'],max_length)
        final_result[j]['track']['artists'][0]['name'] = Utils.truncate_string(i['track']['artists'][0]['name'],max_length)
        j = j + 1

    j = 0
    for i in final_result2:
        final_result2[j]['name'] = Utils.truncate_string(i['name'],max_length)
        final_result2[j]['artists'][0]['name'] = Utils.truncate_string(i['artists'][0]['name'],max_length)
#            print( i[ 'id' ] )//これをデータベースに入れる
        j = j + 1

    j = 0
    for i in final_result3:
        final_result3[j]['name'] = Utils.truncate_string(i['name'],max_length)
        final_result3[j]['artists'][0]['name'] = Utils.truncate_string(i['artists'][0]['name'],max_length)
        j = j + 1

    content = {
        "results":final_result,
        "results2":final_result2,
        "results3":final_result3,
        "IsLogin":IsLogin,
        "data":UserData
    }

    return render(request,'cwm/index.html',content)

def create( request, idn ):
    if request.method == 'POST':
        c = Comment( comment_user_mail=UserData[ 0 ].user_mail, comment_music_id=idn, comment_good=0, comment_text=request.POST[ 'comment_text' ] )
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
    MusHistory = HistoryList(history_user_mail = UserData[0].user_mail,history_music_id = idn)
    MusHistory.save()
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
        'db': UserData[ 0 ],#ログイン中のユーザ情報( 仮 )
        'model': mdl,
        'is_comment': False,
        'data': UserData,#Base内のユーザー情報
        'IsLogin':IsLogin,#Base内のユーザー情報
    }
    if Comment.objects.filter( comment_music_id=idn ).exists():
        content[ 'is_comment' ] = True
        comments = Comment.objects.filter( comment_music_id=idn )
        for i in range( comments.count() ):
            users.append( User.objects.get( user_mail=comments[ i ].comment_user_mail ) )#一つしかとってきてない
            tags.extend( Utils.sharp( comments[ i ].comment_text ) )
            tmp = {
                'user_name': users[ i ].user_name,
                'user_mail': users[ i ].user_mail,
                'user_image': users[ i ].user_image,
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
    max_length = 13
    artist_result = SPOTIFY.artist( id )
    artist_track = SPOTIFY.artist_top_tracks( id, country='JP' )
    result=artist_track['tracks']
    artist_album = SPOTIFY.artist_albums(id, album_type=None, country='JP', limit=50, offset=0)

    j = 0
    for i in result:
        result[j]['name'] = Utils.truncate_string(i['name'],max_length)
        result[j]['artists'][0]['name'] = Utils.truncate_string(i['artists'][0]['name'],max_length)
        j = j + 1

    content = {
        'artist': artist_result,
        'results': result,
        'artist_album': artist_album,
    }
    return render( request, 'cwm/artist.html', content )

def album( request, id ):
    
    albums = SPOTIFY.albums( [ id ], market=None )
    print( albums[ 'albums' ][ 0 ][ 'name' ] )
    content = {
        'album_tracks': albums[ 'albums' ][ 0 ][ 'tracks' ][ 'items' ],
        'album_desc': albums[ 'albums' ][ 0 ],
    }
    return render( request, 'cwm/album.html', content )