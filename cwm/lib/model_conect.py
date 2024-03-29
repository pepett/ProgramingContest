from cwmapp.models import CustomUser, Comment, HistoryList, LikeList, Music, Album, Star, Good ,Reply, GoodComment, GoodCommentReply
from lib.spotify_conect import SPOTIFY

class ModelMus:
    @staticmethod
    @staticmethod
    def C_OGTrack(id):
        #オリジナルソングの配列
        music_tbl = Music.objects.get( music_id = id )
        album_tbl = Album.objects.get( album_id = music_tbl.music_album_id )
        artist_tbl = CustomUser.objects.get( userid = album_tbl.album_userid )
        result = {
            'album': {
                'id': album_tbl.album_id,
                'name': album_tbl.album_name,
                'images':[
                    {
                        'url': album_tbl.album_image.url,
                    },
                ],
            },
            'artists':[
                {
                    'id': artist_tbl.userid,
                    'name': artist_tbl.username,
                },
            ],
            'id': id,
            'name':music_tbl.music_name,
            'preview_url': music_tbl.music_track_preview.url,
            'full_url': music_tbl.music_track_full.url,
            'uri': 'None',
            "ispremium":'premium' if artist_tbl.is_premium else 'not_premium',
        }
        
        return result
    
    def C_OGAlbum( id ):
        if not Album.objects.filter( album_id = id ).exists(): return { 'id': 'None','name':'存在しないユーザ' }
        album_tbl = Album.objects.get( album_id = id )
        artist_tbl = CustomUser.objects.get( userid = album_tbl.album_userid )
        result = {
            'id': album_tbl.album_id,
            'name': album_tbl.album_name,
            'images':[
                {
                    'url': album_tbl.album_image.url,
                },
            ],
            'artists':[
                {
                    'id': artist_tbl.userid,
                    'name': artist_tbl.username,
                },
            ],
            "ispremium":'premium' if artist_tbl.is_premium else 'not_premium',
        }
        return result

    def C_OGArtist( id ):
        if not CustomUser.objects.filter( userid = id ).exists(): return { 'id': None, 'name': '存在しないユーザ' }
        artist_tbl = CustomUser.objects.get( userid = id )
        result = {
            'id': artist_tbl.userid,
            'name': artist_tbl.username,
            'images':[
                {
                    'url': artist_tbl.image.url,
                },
            ],
            "ispremium":'premium' if artist_tbl.is_premium else 'not_premium',
        }
        return result
    
    def setHistory(id):

        Mus = HistoryList.objects.filter(history_userid = id)
        result = []
        
        for i in range(Mus.count()):
            for j in range(Mus.count())[i + 1:]:
                if Mus[i].history_music_id == Mus[j].history_music_id:
                    print('Mus:'+str(i)+':'+str(j))
                    print('music_id:'+Mus[i].history_music_id+':'+Mus[j].history_music_id)
                    Mus[i].delete()
                    break
        
        for i in Mus:
            if len(i.history_music_id) == 25:
                x = ModelMus.C_OGTrack(i.history_music_id)
            else:
                x = SPOTIFY.track(i.history_music_id)
            result.append(x)

        result.reverse()

        return result

    @staticmethod
    def setLiked(id):

        Mus = LikeList.objects.filter(like_userid = id)
        result = []
        
        for i in range(Mus.count()):
            for j in range(Mus.count())[i + 1:]:
                if Mus[i].like_music_id == Mus[j].like_music_id:
                    print('Mus:'+str(i)+':'+str(j))
                    print('music_id:'+Mus[i].like_music_id+':'+Mus[j].like_music_id)
                    Mus[i].delete()
                    break
        
        for i in Mus:
            if len(i.like_music_id) == 25:
                x = ModelMus.C_OGTrack(i.like_music_id)
            else:
                x = SPOTIFY.track(i.like_music_id)
            result.append(x)

        result.reverse()

        return result
    
    @staticmethod
    def setCommented(id):

        Mus = Comment.objects.filter(comment_userid = id)
        result = []
        
        for i in range(Mus.count()):
            for j in range(Mus.count())[i + 1:]:
                if Mus[i].comment_music_id == Mus[j].comment_music_id:
                    print('Mus:'+str(i)+':'+str(j))
                    print('music_id:'+Mus[i].comment_music_id+':'+Mus[j].comment_music_id)
                    Mus[i].delete()
                    break
        
        for i in Mus:
            if len(i.comment_music_id) == 25:
                x = ModelMus.C_OGTrack(i.comment_music_id)
            else:
                x = SPOTIFY.track(i.comment_music_id)
            result.append(x)

        result.reverse()

        return result
    
    @staticmethod
    def setStars(id):

        Mus = Star.objects.filter(star_userid = id)
        result = []
        
        for i in range(Mus.count()):
            for j in range(Mus.count())[i + 1:]:
                if Mus[i].star_music_id == Mus[j].star_music_id:
                    print('Mus:'+str(i)+':'+str(j))
                    print('music_id:'+Mus[i].star_music_id+':'+Mus[j].star_music_id)
                    Mus[i].delete()
                    break
        
        for i in Mus:
            if len(i.star_music_id) == 25:
                x = ModelMus.C_OGTrack(i.star_music_id)
            else:
                x = SPOTIFY.track(i.star_music_id)
            result.append(x)

        result.reverse()

        return result
    
    @staticmethod
    def DeleteMus(idn):
        Mus = Music.objects.get(music_id = idn)
        MusHistory = HistoryList.objects.filter(history_music_id = idn).delete()
        MusLiked = LikeList.objects.filter(like_music_id = idn).delete()
        CommentData = Comment.objects.filter( comment_music_id=idn)
        StarData = Star.objects.filter( star_music_id = idn).delete()
        GoodData = Good.objects.filter( good_music_id = idn).delete()
        AlbumData = Album.objects.filter( album_id = Mus.music_album_id)
        for i in CommentData:
            ReplyData = Reply.objects.filter( reply_comment_id = i.comment_id)
            GoodCommentData = GoodComment.objects.filter( gc_comment_id = i.comment_id)
            ReplyData.delete()
            GoodCommentData.delete()
        CommentData.delete()
        for i in AlbumData:
            i.album_image.delete()
            i.delete()
        Mus.music_track_full.delete()
        Mus.music_track_preview.delete()
        Mus.delete()