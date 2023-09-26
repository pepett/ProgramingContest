import os
import re
import json
import uuid
import pprint
import bleach
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password,check_password
from lib.spotify_conect import SPOTIFY
from lib.utils import Utils
from lib.model_conect import ModelMus
from cwmapp.models import Comment, HistoryList, LikeList, Music, Album, Star, Good ,Reply, GoodComment, GoodCommentReply

from .forms import CommentForm, UploadImageForm, UsernameForm, RegisterForm, CustomUser, MusicRegisterForm, AlbumRegisterForm#, LoginForm

# Create your views here.

#仮ログイン
#IsLogin = True
#UserData = User.objects.filter( user_mail = 'k228021@kccollege.ac.jp' )

def top( request ):
    #例ここから 
    #tmp = Utils.sharp( "unti unti #aaaa \n un#ti #bbb jsflkdsj" )
    #for counter in range( len( tmp ) ):
    #    print( tmp[ counter ] )
    #例ここまで
    if request.user.is_authenticated:
        User = CustomUser.objects.filter( userid = request.user.userid )
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
    if request.user.is_authenticated:
        return redirect(index)
    
    if request.POST:
        img = Utils.CreateUserImage(request.POST['username'],str(Utils.randomid()))
        register_form = RegisterForm( request.POST)
        if register_form.is_valid():
            reg = register_form.save()
            email = reg.email
            password = reg.password
            reg.set_password( reg.password )
            reg.image = img
            reg.save()
            content = {
                'register_form': register_form
            }
            user = authenticate( request, email=email, password=password )

            if user is not None:
                login( request, user )
                Utils.sendemailregister(request)
                
                return redirect( 'index' )
            else:
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
    
    User = CustomUser.objects.filter( userid = request.user.userid )
    Likeresult = []
    Historyresult = []
    MyAlbum = []
    MyMusic = []
    Uploadresult = []

    if Album.objects.filter(album_userid = request.user.userid):
        MyAlbum = Album.objects.filter(album_userid = request.user.userid)
        for j in MyAlbum:
            MyMusic = Music.objects.filter(music_album_id = j.album_id)
            for i in MyMusic:

                Uploadresult.append({
                    "music_track_preview_url":i.music_track_preview.url,
                    "music_track_full_url":i.music_track_full.url,
                    "music_id":i.music_id,
                    "album_image_url":MyAlbum.get(album_id = i.music_album_id).album_image.url,
                    "music_name":i.music_name,
                    "album_userid":MyAlbum.get(album_id = i.music_album_id).album_userid,
                    "name":User.get(userid = MyAlbum.get(album_id = i.music_album_id).album_userid).username,
                    "ispremium":User.get(userid = MyAlbum.get(album_id = i.music_album_id).album_userid).is_premium
                    })
        
        print(Uploadresult)
        Uploadresult.reverse()


    content = {
        "results":Likeresult,
        "results2":Historyresult,
        "upload_form":UploadImageForm(),
        "Uploadresult":Uploadresult,
        "data":User,
        "username_form":UsernameForm(),
        "MyAlbum":MyAlbum,
        "MyMusic":MyMusic,
        "id":None
    }

    MusHistory = HistoryList.objects.filter(history_userid = request.user.userid)
    MusLiked = LikeList.objects.filter(like_userid = request.user.userid)
    CommentData = Comment.objects.filter( comment_userid=request.user.userid)
    StarData = Star.objects.filter( star_userid = request.user.userid)
    GoodData = Good.objects.filter( good_userid = request.user.userid)
    ReplyData = Reply.objects.filter( reply_userid = request.user.userid)

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
        
        return redirect('setting')

    Historyresult = ModelMus.setHistory(request.user.userid)
    Likeresult = ModelMus.setLiked(request.user.userid)

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
        User = CustomUser.objects.filter( userid = request.user.userid )

    for i in nres:
        i_nr = Comment.objects.get( comment_id = str( i ) )
        t = {}
        if len( i_nr.comment_music_id ) == 25:
            music_tbl = Music.objects.get( music_id = i_nr.comment_music_id )
            albm_tbl = Album.objects.get( album_id = music_tbl.music_album_id )
            artt_tbl = CustomUser.objects.get( userid = albm_tbl.album_userid )
            t = {
                'c_music': ModelMus.C_OGTrack( i_nr.comment_music_id ),
                'c_text' : i_nr.comment_text,
            }
        else:
            t = {
                'c_music': SPOTIFY.track( i_nr.comment_music_id, market=None ),
                'c_text': i_nr.comment_text
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
        "like": [],
        "tags": [],
        "history": [],
        "comment_mus": [],
        "good_mus": [],
        "ucomment_mus": [],
        "star_mus": [],
        "oridinal": [],
        "data":User,
    }
    
    if request.user.is_authenticated:
        User = CustomUser.objects.filter( userid = request.user.userid )
        content[ 'data' ] = User

    original_tracks = []
    if Music.objects.all().count() != 0:
        for i in Music.objects.all():
            albm_tbl = Album.objects.get( album_id = i.music_album_id )
            artt_tbl = CustomUser.objects.get( userid = albm_tbl.album_userid )
            if (CustomUser.objects.get(userid = albm_tbl.album_userid).is_premium):
                original_tracks.append( {
                    'album' : {
                        'id' : albm_tbl.album_id,
                        'name' : albm_tbl.album_name,
                        'img' : [
                            {
                                'url' :albm_tbl.album_image.url,
                            },
                        ],
                    },
                    'artists' : [
                        {
                            'id' : artt_tbl.userid,
                            'name' : artt_tbl.username,
                        }
                    ],
                    'id' : i.music_id,
                    'name' : i.music_name,
                    'preview_url' :i.music_track_preview.url,
                    'full_url' :i.music_track_full.url,
                    'uri' : None,
                    "ispremium":"premium",
                })
            else:
                original_tracks.append( {
                    'album' : {
                        'id' : albm_tbl.album_id,
                        'name' : albm_tbl.album_name,
                        'img' : [
                            {
                                'url' :albm_tbl.album_image.url,
                            },
                        ],
                    },
                    'artists' : [
                        {
                            'id' : artt_tbl.userid,
                            'name' : artt_tbl.username,
                        }
                    ],
                    'id' : i.music_id,
                    'name' : i.music_name,
                    'preview_url' :i.music_track_preview.url,
                    'full_url' :i.music_track_full.url,
                    'uri' : None,
                    "ispremium":"not_premium",
                })

    content[ "oridinal" ] = original_tracks
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
            
            if len(i) == 25:
                
                stars.append( {
                    'star': ave,
                    'track': ModelMus.C_OGTrack(i),
                } )
            else:
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

    #コメントの件数が多い曲
    if Comment.objects.all().exists():
        cmt_all = Comment.objects.all()
        cmt_mus_id = []
        cmt_mus_track = []
        for i in cmt_all:
            cmt_mus_id.append( i.comment_music_id )
        cmt_mus_data = Utils.n_dup( cmt_mus_id )
        for i in cmt_mus_data:
            if len(i[ 'tag_name' ]) == 25:
                cmt_mus_track.append( { 'track': ModelMus.C_OGTrack(i[ 'tag_name' ]), 'num': i[ 'tag_num' ] } )
            else:
                cmt_mus_track.append( { 'track': SPOTIFY.track( i[ 'tag_name' ], market=None ), 'num': i['tag_num'] } )
        content[ 'comment_mus' ] = cmt_mus_track

            
    #いいね数が多い曲
    if Good.objects.all().exists():
        good_all = Good.objects.all()
        good_mus_id = []
        good_mus_track = []
        for i in good_all:
            if i.good_bool:
                good_mus_id.append( i.good_music_id )
        good_mus_id = Utils.n_dup( good_mus_id )
        for i in good_mus_id:
            if len(i[ 'tag_name' ]) == 25:
                good_mus_track.append( { 'track': ModelMus.C_OGTrack(i[ 'tag_name' ]), 'num': i[ 'tag_num' ] } )
            else:
                good_mus_track.append( { 'track': SPOTIFY.track( i[ 'tag_name' ], market=None ), 'num': i[ 'tag_num' ] } )
        content[ 'good_mus' ] = good_mus_track

    if request.user.is_authenticated:
        #最近見た曲
        if HistoryList.objects.filter( history_userid = request.user.userid ).exists():
            content[ 'history' ] = ModelMus.setHistory(request.user.userid)
        #いいねした曲
        if Good.objects.filter( good_userid = request.user.userid ).exists():
            content[ 'like' ] = ModelMus.setLiked(request.user.userid)

        #コメントした曲
        if Comment.objects.filter( comment_userid = request.user.userid ).exists():
            content[ 'ucomment_mus' ] = ModelMus.setCommented(request.user.userid)

        #評価した曲
        if Star.objects.filter( star_userid = request.user.userid ).exists():
            content[ 'star_mus' ] = ModelMus.setStars(request.user.userid)

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
        clean_text = bleach.clean( request.POST[ 'comment_text' ] )
        c = Comment( comment_userid=request.user.userid, comment_music_id=idn, comment_text=clean_text )
        c.save()
    return redirect( 'mus', idn )

def create( request, idn ):
    if request.method == 'POST':
        c = Comment( comment_userid=request.user.userid, comment_music_id=idn, comment_text=request.POST[ 'comment_text' ] )
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
    if request.user.is_authenticated:#ログイン時にしか使えない機能
        if Star.objects.filter( star_userid = request.user.userid, star_music_id = idn ).exists():
            user_star = Star.objects.get( star_userid = request.user.userid, star_music_id = idn ).star_num
        if Good.objects.filter( good_music_id = idn, good_userid = request.user.userid ).exists():
            good_count = Good.objects.get(good_music_id = idn, good_userid = request.user.userid ).good_bool
            for i in Good.objects.filter(good_music_id = idn):
                good_count = Good(good_userid = request.user.userid, good_music_id = idn )
        if Good.objects.filter(good_userid = request.user.userid , good_music_id = idn ).exists():
            good_bool = Good.objects.get(good_userid = request.user.userid , good_music_id = idn ).good_bool
    if Good.objects.filter( good_music_id = idn ).exists():
        good_count = Good.objects.filter( good_music_id = idn, good_bool = True).count()


    #CWMオリジナル曲かの判定
    track_result = {}
    flg = False
    if len( idn ) == 25:
        music_tbl = Music.objects.get( music_id = idn )
        album_tbl = Album.objects.get( album_id = music_tbl.music_album_id )
        artist_tbl = CustomUser.objects.get( userid = album_tbl.album_userid )
        #artists = []
        
        track_result = {
            'album': {
                'id': album_tbl.album_id,
                'name': album_tbl.album_name,
                'img':[
                    {
                        'url': album_tbl.album_image,
                    },
                ],
            },
            'artists':[
                {
                    'id': artist_tbl.userid,
                },
            ],
            'id': idn,
            'name':music_tbl.music_name,
            'preview_url': music_tbl.music_track_preview,
            'full_url': music_tbl.music_track_full,
            'uri': 'None',
        }
        flg = True
    else:
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
        'is_original': flg,
    }

    if request.user.is_authenticated:
        User = CustomUser.objects.filter( userid = request.user.userid )
        content[ 'data' ] = User
        MusHistory = HistoryList(history_userid = request.user.userid,history_music_id = idn)
        MusHistory.save()
        ModelMus.setHistory(request.user.userid)

    if Comment.objects.filter( comment_music_id=idn ).exists():
        content[ 'is_comment' ] = True
        comments = Comment.objects.filter( comment_music_id=idn )
        for i in range( comments.count() ):
            users.append( CustomUser.objects.get( userid=comments[ i ].comment_userid ) )#一つしかとってきてない
            tags.extend( Utils.sharp( comments[ i ].comment_text ) )
            
            tmp = {
                'user_name': users[ i ].username,
                'user_id': users[ i ].userid,
                'user_image': users[ i ].image,
                'comment_id': comments[ i ].comment_id,
                'comment_good': GoodComment.objects.filter( gc_comment_id = comments[ i ].comment_id, gc_bool = True ).count(),
                'is_good': False,
                'comment_text': comments[ i ].comment_text,
                'comment_posted': comments[ i ].comment_posted,
                'result': results
            }
            if request.user.is_authenticated:
                if GoodComment.objects.filter( gc_userid = request.user.userid, gc_comment_id = comments[ i ].comment_id ).exists():
                    tmp[ 'is_good' ] = GoodComment.objects.get( gc_userid = request.user.userid, gc_comment_id = comments[ i ].comment_id ).gc_bool
            
            mdl.append( tmp )
        
        #tags = Utils.del_duplicate( tags, False )
        data = Utils.n_dup( tags )
        
        content[ 'tags' ] = data
        content[ 'comments' ] = comments
        content[ 'users' ] = users
    return render( request, 'cwm/music.html', content )

def search( request ):
    #if len( request.GET[ 'search-music' ] ) != 0:
    if request.user.is_authenticated:
        User = CustomUser.objects.filter( userid = request.user.userid )
        content = {
            'tags': '',
            'data':User,
            'top10': None,
        }
    else:
        content = {
            'tags': '',
            'data':None,
            'top10': None,
        }

    if Comment.objects.all().exists():#タグを表示
        cmts = Comment.objects.all()
        tags = []
        for i in cmts:
            tags.extend( Utils.sharp( i.comment_text ) )
        data = Utils.n_dup( tags )
        content[ 'tags' ] = data
    
    playlist_uri = 'spotify:playlist:7t47MzpvKe00KAYZ60qGl3'
    results = SPOTIFY.playlist_tracks( playlist_uri )[ 'items' ]
    top10 = results[ :30 ]
    content[ 'top10' ] = top10

    return render( request, 'cwm/search.html', content )


def artist( request, id ):

    artist_result = []
    result = []
    artist_album = []
    related_artist = []
    User = False

    if len( id ) == 25:
        return redirect('user',id)

    content = {
        'artist': artist_result,
        'results': result,
        'artist_album': artist_album,
        'related_artist': related_artist,
        'data': User
    }
    if request.user.is_authenticated:
        User = CustomUser.objects.filter( userid = request.user.userid )
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
        'data':User,
        'is_original' : False,
    }

    if request.user.is_authenticated:
        User = CustomUser.objects.filter( userid = request.user.userid )

    if len( id ) == 25:
        content[ 'is_original' ] = True
        albm_tbl = Album.objects.get( album_id = id )
        artt_tbl = CustomUser.objects.get( userid = albm_tbl.album_userid )
        artist_album = {
            'image' : [
                {
                    'url' : albm_tbl.album_image,
                },
            ],
            'name' : albm_tbl.album_name,
            'artists' : {
                'name' : artt_tbl.username,
                'id' : artt_tbl.userid,
            }
        }
        for i in Music.objects.filter( music_album_id = id ):
            album_items.append( {
                'name' : i.music_name,
                'id' : i.music_id,
                'preview_url' : i.music_track_preview,
                'artists' : {
                    'name' : artt_tbl.username,
                    'id' : artt_tbl.userid,
                },
            } )
    else:
        albums = SPOTIFY.albums( [ id ], market=None )
        artist_album = albums['albums'][0]
        album_items = albums['albums'][0]['tracks']['items']


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
            if Star.objects.filter( star_userid = request.user.userid, star_music_id = idn ).exists():#データの存在確認
                g_s = Star.objects.get( star_userid = request.user.userid, star_music_id = idn )#個人の評価
                st = data[ 'number' ] + 1#jsから送られてきた数値
                g_s.star_num = st#評価をデータベースに入れる
                g_s.save()#データベースをセーブ
            else:#まだ評価していないデータの場合
                st = data[ 'number' ] + 1#
                g_s = Star( star_userid = request.user.userid, star_music_id = idn, star_num = st )
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
            if Good.objects.filter( good_userid = request.user.userid, good_music_id = idn ).exists():
                good = Good.objects.get( good_userid = request.user.userid, good_music_id = idn )#取得
                good.good_bool = not good.good_bool
                
                if good.good_bool == True:
                    MusLike = LikeList(like_userid = request.user.userid,like_music_id = idn)
                    MusLike.save()
                    ModelMus.setHistory(request)
                else:
                    MusLiked = LikeList.objects.get(like_userid = request.user.userid,like_music_id = idn)
                    MusLiked.delete()
                good.save()
            else:
                # データが未登録の場合
                good = Good.objects.create(good_userid=request.user.userid, good_music_id=idn)
                good.good_bool = not good.good_bool
                good.save()
                MusLike = LikeList(like_userid = request.user.userid,like_music_id = idn)
                MusLike.save()
                ModelMus.setHistory(request)
            #print(Good.objects.get( good_userid = request.user.userid, good_music_id = idn ).good_bool)
        content = {
            'good_count':Good.objects.filter(good_music_id = idn, good_bool = True).count(),
            'good_bool':str(Good.objects.get( good_userid = request.user.userid, good_music_id = idn ).good_bool).lower(),
        }

        return JsonResponse( content ) 

def good_comment( request, idn ):
    content = {}
    if request.POST:
        if request.user.is_authenticated:

            if GoodComment.objects.filter( gc_userid = request.user.userid, gc_comment_id = idn ).exists():
                gc = GoodComment.objects.get( gc_userid = request.user.userid, gc_comment_id = idn )
                gc.gc_bool = not gc.gc_bool
                gc.save()
            else:
                gc = GoodComment.objects.create( gc_userid = request.user.userid, gc_comment_id = idn )
                gc.gc_bool = not gc.gc_bool
                gc.save()
            content = {
                'gc_count': GoodComment.objects.filter( gc_comment_id = idn, gc_bool = True ).count(),
                'gc_bool':str( GoodComment.objects.get( gc_userid = request.user.userid, gc_comment_id = idn ).gc_bool ).lower(),
            }
            return JsonResponse( content )

def create_reply( request, idn, cid ):
    if request.POST:
        clean_text = bleach.clean( request.POST[ 'reply-text' ] )
        r = Reply( reply_comment_id = cid, reply_userid = request.user.userid, reply_text = clean_text )
        r.save()
        return redirect( 'mus', idn )

def view_reply( request, idn ):
    if request.POST:
        length = 0
        contents = []
        if Reply.objects.filter( reply_comment_id = idn ).exists():
            reply = Reply.objects.filter( reply_comment_id = idn )
            for i in reply:
                user = CustomUser.objects.get( userid = i.reply_userid )
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
        User = CustomUser.objects.filter( userid = request.user.userid )
    else:
        return redirect( 'Login' )

    if request.method == 'POST':
            if 'oldpassword' in request.POST and 'newpassword' in request.POST:
                OldPassword = request.POST['oldpassword']
                NewPassword = request.POST['newpassword']
                userID = request.user.userid
                if check_password(OldPassword,User[0].password):
                    User.update(password = make_password(NewPassword))
                    User = authenticate( request, userid=userID, password=NewPassword)
                    if User is not None:
                        login( request, User )
                        return redirect( 'setting' )
                    else:
                        return redirect( 'top' )
    content = {
        'data':User
    }

    return render( request, 'cwm/changepassword.html', content )

def upload( request):
    
    User = False
    albums = []

    if request.user.is_authenticated:
        User = CustomUser.objects.filter( userid = request.user.userid )
        albums = Album.objects.filter( album_userid = request.user.userid)

    else:
        return redirect( 'Login' )
    
    if request.method == 'POST':
        radio = request.POST.get('SelectAlbum')
        request.POST._mutable = True
        request.POST['album_userid'] = request.user.userid
        request.POST._mutable = False
        print(request.POST)

        if radio == 'MakeAlbum':
            AlbumForm = AlbumRegisterForm(request.POST,request.FILES)
            if AlbumForm.is_valid():
                AlbumForm.save()
                print(AlbumForm.instance.album_id)

            request.POST._mutable = True
            request.POST['music_album_id'] = AlbumForm.instance.album_id
            request.POST._mutable = False
            print(request.POST)
            MusicForm = MusicRegisterForm(request.POST,request.FILES)
            if MusicForm.is_valid():
                MusicForm.save()
            print('MakeAlbum')
        elif radio == 'Single':
            request.POST._mutable = True
            request.POST['album_name'] = request.POST['music_name']
            request.POST._mutable = False
            AlbumForm = AlbumRegisterForm(request.POST,request.FILES)
            if AlbumForm.is_valid():
                AlbumForm.save()
                print(AlbumForm.instance.album_id)

            request.POST._mutable = True
            request.POST['music_album_id'] = AlbumForm.instance.album_id
            request.POST._mutable = False
            print(request.POST)
            MusicForm = MusicRegisterForm(request.POST,request.FILES)
            if MusicForm.is_valid():
                MusicForm.save()
            print('Single')
        else:
            request.POST._mutable = True
            request.POST['music_album_id'] = radio
            request.POST._mutable = False
            MusicForm = MusicRegisterForm(request.POST,request.FILES)
            if MusicForm.is_valid():
                MusicForm.save()
            print('Else')

        return redirect( 'setting' )

    content = {
        'MusicRegisterForm':MusicRegisterForm(),
        'AlbumRegisterForm':AlbumRegisterForm(),
        'Albums':albums,
        'data':User,
    }

    return render( request, 'cwm/upload.html', content )

def user(request,idn):
    
    User = False
    Page_User = []
    MyAlbum = []
    MyMusic = []
    Uploadresult = []
    Likeresult = []

    if request.user.is_authenticated:
        User = CustomUser.objects.filter( userid = request.user.userid )

    if CustomUser.objects.filter( userid = idn ):
        Page_User = CustomUser.objects.filter( userid = idn )
        Likeresult = ModelMus.setLiked(idn)

        if Album.objects.filter(album_userid = idn):
            MyAlbum = Album.objects.filter(album_userid = idn)
            for j in MyAlbum:
                MyMusic = Music.objects.filter(music_album_id = j.album_id)
                for i in MyMusic:

                    Uploadresult.append({
                        "music_track_preview_url":i.music_track_preview.url,
                        "music_track_full_url":i.music_track_full.url,
                        "music_id":i.music_id,
                        "album_image_url":MyAlbum.get(album_id = i.music_album_id).album_image.url,
                        "music_name":i.music_name,
                        "album_userid":MyAlbum.get(album_id = i.music_album_id).album_userid,
                        "name":Page_User.get(userid = MyAlbum.get(album_id = i.music_album_id).album_userid).username
                        })
            
            print(Uploadresult)
            Uploadresult.reverse()

    else:
        print('No Data')

    content = {
        'artist':Page_User,
        "Uploadresult":Uploadresult,
        'LikedMus':Likeresult,
        'Albums':MyAlbum,
        'data':User,
    }

    return render( request, 'cwm/user.html', content )

def premium_descreption( request ):
    return render( request, 'cwm/premium_descreption.html' )
def tos( request ):
    return render( request, 'cwm/tos.html' )

def register_premium( request ):
    if request.user.is_authenticated:
        Utils.sendmail_premium( request )#ユーザに対する報告メール
        Utils._sendmail_premium( request )#管理者に対する報告メール
        return redirect( 'top' )
    else:
        return redirect( 'register' )