import os
import re
import json
import uuid
import pprint
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password,check_password
from lib.spotify_conect import SPOTIFY
from lib.utils import Utils
from lib.model_conect import ModelMus
from cwmapp.models import User, Comment, HistoryList, LikeList, Music, Star, Good ,Reply

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
        User = CustomUser.objects.filter( email = request.user.email )
        print( request.user.last_login )

        content = {
            'data':User,
        }
    else:
        content = {
            'data':None,
        }
    
    return render( request, 'cwm/top.html' ,content)

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
        img = Utils.CreateUserImage(request.POST['username'],str(uuid.uuid4()))
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

    MusHistory = HistoryList.objects.filter(history_user_mail = request.user.email)
    MusLiked = LikeList.objects.filter(like_user_mail = request.user.email)
    CommentData = Comment.objects.filter( comment_user_mail=request.user.email)
    StarData = Star.objects.filter( star_user_mail = request.user.email)
    GoodData = Good.objects.filter( good_user_mail = request.user.email)
    ReplyData = Reply.objects.filter( reply_user_mail = request.user.email)

    if (request.method == 'POST'):

        if 'UserDlt' in request.POST:#ユーザー削除ボタンを押した場合
            CommentData.delete()#コメントの削除
            StarData.delete()#つけた★の削除
            ReplyData.delete()#リプライの削除
            MusHistory.delete()#履歴の削除
            MusLiked.delete()#いいねの削除
            User[0].image.delete()#ユーザーアイコンの削除
            User.delete()#ユーザーデータの削除
            return redirect( 'top' )

        elif 'UserSubmit' in request.POST:
            if (request.FILES):
                UpdateFileName = User[0].userid+os.path.splitext(request.FILES['image'].name)[1]
                if (request.POST['NewUsername']):
                    NewUsername = request.POST['NewUsername']
                    User.update(username = NewUsername)
                    #print('UpdateFileName1'+UpdateFileName)
                else:
                    print('UpdateFileName2'+UpdateFileName)
                request.FILES['image'].name = UpdateFileName
                User[0].image.delete()
                image = UploadImageForm(request.POST,request.FILES)
                image.save()
                User.update(image = 'images/'+UpdateFileName)

            elif(request.POST['NewUsername']):
                NewUsername = request.POST['NewUsername']
                User.update(username = NewUsername)

    Historyresult = ModelMus.setHistory(request)
    Likeresult = ModelMus.setLiked(request)

    content['results'] = Likeresult[:30]
    content['results2'] = Historyresult[:30]
    content['user'] = User
    return render(request,'cwm/setting.html',content)


def result( request ):
    if not request.GET[ 'search-music' ]:
        return redirect( 'search' )
    res = Comment.objects.filter( comment_text__regex = request.GET[ 'search-music' ] )
    ctracks = []
    User = []
    nres = list( { nr.comment_music_id: nr for nr in res }.values() )#検索に引っかかる時に同じ曲が出ないようにする
    #print( nres )
    #print( res[ 0 ].comment_music_id )
    #重複をなくしたい

    if request.user.is_authenticated:
        User = CustomUser.objects.filter( email = request.user.email )

    for i in nres:
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
        'data':User,
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
        "tags": '',
        "history": [],
        "comment_mus": [],
        "data":User,
    }
    
    if request.user.is_authenticated:
        User = CustomUser.objects.filter( email = request.user.email )
        content[ 'data' ] = User

    max_length = 13
    Playlist_uri = 'spotify:playlist:37i9dQZEVXbKXQ4mDTEBXq'
    
    results = SPOTIFY.playlist_tracks(Playlist_uri)['items']
    final_result = results[:10]

    eval_tracks = Star.objects.order_by( 'star_num' ).reverse()#評価がついてる曲を取得
    eval_track = []#評価がついてる曲(かぶりなし)
    stars = []#評価を格納
    #stars_id = []
    for i in eval_tracks:
        eval_track.append( i.star_music_id )
    eval_track = list( set( eval_track ) )
    for i in eval_track:
        if Star.objects.filter( star_music_id = i ).exists():
            st = Star.objects.filter( star_music_id = i )
            ave = 0
            for j in st:
                ave += j.star_num
            ave /= st.count()
            ave = Utils.round( ave )
            #stars_id.append( i )
            
            stars.append( {
                'star': ave,
                'track': SPOTIFY.track( i, market=None ),
            } )
    #print( sorted( stars, key = lambda x: x[ 'star' ], reverse = True ) )
    '''for i in range( len( stars ) ):
        print( SPOTIFY.track( stars_id[ i ], market=None )[ 'name' ] + str(stars[ i ]) )
        tmp = {
            'star': stars[ i ],
            'track': SPOTIFY.track( stars_id[ i ], market=None ),
        }
        stars[ i ] = tmp

    print( stars[ 0 ][ 'track' ][ 'name' ] )
    
    '''
    
    #lz_uri2 = 'spotify:artist:1snhtMLeb2DYoMOcVbb8iB'
    #results2 = SPOTIFY.artist_top_tracks(lz_uri2)
    #final_result2=results2['tracks']
    final_result2 = sorted( stars, key = lambda x: x[ 'star' ], reverse = True )

    lz_uri3 = 'spotify:artist:5Vo1hnCRmCM6M4thZCInCj'
    results3 = SPOTIFY.artist_top_tracks(lz_uri3)
    final_result3=results3['tracks']

    #コメントの件数
    if Comment.objects.all().exists():
        cmt_all = Comment.objects.all()
        cmt_mus_id = []
        cmt_mus_track = []
        for i in cmt_all:
            cmt_mus_id.append( i.comment_music_id )
        cmt_mus_data = Utils.n_dup( cmt_mus_id )
        for i in cmt_mus_data:
            cmt_mus_track.append( { 'track': SPOTIFY.track( i['tag_name'], market=None ),'num': i['tag_num'] } )
        content[ 'comment_mus' ] = cmt_mus_track

            
    #履歴
    if request.user.is_authenticated:
        if HistoryList.objects.filter( history_user_mail = request.user.email ).exists():
            his = HistoryList.objects.filter( history_user_mail = request.user.email )
            nhis = []
            for i in his:
                nhis.append( SPOTIFY.track( i.history_music_id, market=None ) )
            
            nhis.reverse()
            content[ 'history' ] = nhis

    #タグを表示
    if Comment.objects.all().exists():
        cmts = Comment.objects.all()
        tags = []
        for i in cmts:
            tags.extend( Utils.sharp( i.comment_text ) )
        data = Utils.n_dup( tags )
        content[ 'tags' ] = data

    content['results'] = final_result
    content['results2'] = final_result2
    content['results3'] = final_result3

    return render(request,'cwm/index.html',content)

def create( request, idn ):
    if request.method == 'POST':
        c = Comment( comment_user_mail=request.user.email, comment_music_id=idn, comment_good=0, comment_text=request.POST[ 'comment_text' ] )
        c.save()
    return redirect( 'mus', idn )

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
    good_bool = False
    good_count = 0
    if Star.objects.filter( star_music_id = idn ).exists():
        for i in range( Star.objects.filter( star_music_id = idn ).count() ):
            ave_star += Star.objects.filter( star_music_id = idn )[ i ].star_num
        ave_star /= Star.objects.filter( star_music_id = idn ).count()
        ave_star = Utils.round( ave_star )
    if request.user.is_authenticated:
        if Star.objects.filter( star_user_mail = request.user.email, star_music_id = idn ).exists():
            user_star = Star.objects.get( star_user_mail = request.user.email, star_music_id = idn ).star_num
        if Good.objects.filter( good_music_id = idn, good_user_mail = request.user.email ).exists():
            good_count = Good.objects.get(good_music_id = idn, good_user_mail = request.user.email ).good_bool
            for i in Good.objects.filter(good_music_id = idn):
                good_count = Good(good_user_mail = request.user.email, good_music_id = idn )
        if Good.objects.filter(good_user_mail = request.user.email , good_music_id = idn ).exists():
            good_bool = Good.objects.get(good_user_mail = request.user.email , good_music_id = idn ).good_bool
    if Good.objects.filter( good_music_id = idn ).exists():
        good_count = Good.objects.filter( good_music_id = idn, good_bool = True).count()

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
        'good_count': good_count,
        'good_bool':good_bool,
    }

    if request.user.is_authenticated:
        User = CustomUser.objects.filter( email = request.user.email )
        content[ 'data' ] = User
        MusHistory = HistoryList(history_user_mail = request.user.email,history_music_id = idn)
        MusHistory.save()
        ModelMus.setHistory(request)

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
        
        #tags = Utils.del_duplicate( tags, False )
        data = Utils.n_dup( tags )
        
        content[ 'tags' ] = data
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
    if request.user.is_authenticated:
        User = CustomUser.objects.filter( email = request.user.email )
        content = {
            'tags': '',
            'data':User,
        }
    else:
        content = {
            'tags': '',
            'data':None,
        }

    if Comment.objects.all().exists():#タグを表示
        cmts = Comment.objects.all()
        tags = []
        for i in cmts:
            tags.extend( Utils.sharp( i.comment_text ) )
        data = Utils.n_dup( tags )
        content[ 'tags' ] = data
    return render( request, 'cwm/search.html', content )

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
    result = artist_track['tracks']
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

    artist_album = []
    album_items = []
    User = False
        
    content = {
        'artist_album': artist_album,
        'album_items': album_items,
        'data':User
    }

    if request.user.is_authenticated:
        User = CustomUser.objects.filter( email = request.user.email )

    albums = SPOTIFY.albums( [ id ], market=None )
    artist_album = albums['albums'][0]
    album_items = albums['albums'][0]['tracks']['items']

    print(artist_album)


    content[ 'artist_album' ] = artist_album
    content[ 'album_items' ] = album_items
    content[ 'data' ] = User

    return render( request, 'cwm/album.html', content )

def star( request, idn ):#非同期時に行う処理
    if request.POST:
        data = json.loads( request.POST[ 'star_n' ] )#jsonをロード
        ave_star = 0#平均
        user_star = 0#ユーザの評価

        if request.user.is_authenticated:#ログイン判定
            #g_s = None
            if Star.objects.filter( star_user_mail = request.user.email, star_music_id = idn ).exists():#データの存在確認
                g_s = Star.objects.get( star_user_mail = request.user.email, star_music_id = idn )#個人の評価
                st = data[ 'number' ] + 1#jsから送られてきた数値
                g_s.star_num = st#評価をデータベースに入れる
                g_s.save()#データベースをセーブ
            else:#まだ評価していないデータの場合
                st = data[ 'number' ] + 1#
                g_s = Star( star_user_mail = request.user.email, star_music_id = idn, star_num = st )
                g_s.save()
            user_star = g_s.star_num#個人の評価
        if Star.objects.filter( star_music_id = idn ).exists():#データの存在確認
            for i in range( Star.objects.filter( star_music_id = idn ).count() ):#音楽に対する評価の件数回まわす
                ave_star += Star.objects.filter( star_music_id = idn )[ i ].star_num#全部加算
            ave_star /= Star.objects.filter( star_music_id = idn ).count()#平均
            ave_star = Utils.round( ave_star )#四捨五入
        content = {
            'ave_star': ave_star,
            'user_star': user_star,
        }
    return JsonResponse( content )#json形式で返す

def good( request, idn ):#非同期時に行う処理
    if request.POST:

        if request.user.is_authenticated:#ログイン判定
            #ｄｂの変更
            if Good.objects.filter( good_user_mail = request.user.email, good_music_id = idn ).exists():
                good = Good.objects.get( good_user_mail = request.user.email, good_music_id = idn )#取得
                good.good_bool = not good.good_bool
                good.save()

            else:
                # データが未登録の場合
                good = Good.objects.create(good_user_mail=request.user.email, good_music_id=idn)
            #print(Good.objects.get( good_user_mail = request.user.email, good_music_id = idn ).good_bool)
        content = {
            'good_count':Good.objects.filter(good_music_id = idn, good_bool = True).count(),
            'good_bool':str(Good.objects.get( good_user_mail = request.user.email, good_music_id = idn ).good_bool).lower(),
        }

        return JsonResponse( content ) 

def create_reply( request, idn, cid ):
    if request.POST:
        r = Reply( reply_comment_id = cid, reply_user_mail = request.user.email, reply_text = request.POST[ 'reply-text' ] )
        r.save()
        return redirect( 'mus', idn )

def view_reply( request, idn ):
    if request.POST:
        length = 0
        contents = []
        if Reply.objects.filter( reply_comment_id = idn ).exists():
            reply = Reply.objects.filter( reply_comment_id = idn )
            for i in reply:
                user = CustomUser.objects.get( email = i.reply_user_mail )
                data = {
                    'user_name': user.username,
                    'user_image': user.image.url,
                    'reply_id': i.reply_id,
                    'reply_text': i.reply_text,
                    'reply_posted': i.reply_posted,
                    #'reply_good': i.reply_good,
                }
                contents.append( data )
            #contents = Reply.objects.filter( reply_comment_id = idn )
            #contents = serializers.serialize("json", )
            length = Reply.objects.filter( reply_comment_id = idn ).count()
        content = {
            'id': idn,
            'len': length,
            'contents': contents,
        }
    return JsonResponse( content )

def changepassword( request):
    
    User = False

    if request.user.is_authenticated:
        User = CustomUser.objects.filter( email = request.user.email )
    else:
        return redirect( 'Login' )

    if request.method == 'POST':
            if 'oldpassword' in request.POST and 'newpassword' in request.POST:
                OldPassword = request.POST['oldpassword']
                NewPassword = request.POST['newpassword']
                useremail = request.user.email
                if check_password(OldPassword,User[0].password):
                    User.update(password = make_password(NewPassword))
                    User = authenticate( request, email=useremail, password=NewPassword)
                    if User is not None:
                        login( request, User )
                        return redirect( 'setting' )
                    else:
                        return redirect( 'top' )
    content = {
        'data':User
    }

    return render( request, 'cwm/changepassword.html', content )