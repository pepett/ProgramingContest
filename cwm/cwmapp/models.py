from django.db import models

class User( models.Model ):#ユーザーのテーブル
    user_name = models.CharField( max_length = 50 )
    user_mail = models.EmailField( primary_key = True )
    user_pass = models.CharField( max_length = 50 )
    user_image = models.CharField( max_length = 200 )
    user_birthday = models.DateField()

class Music( models.Model ):#曲のテーブル
    music_id = models.AutoField( primary_key = True )
    music_name = models.TextField()
    music_star = models.IntegerField( default = 0 )
    music_image = models.CharField( max_length = 200 )
    music_artistname = models.TextField()
    music_albumname = models.TextField()
    music_preview = models.TextField()
    music_playurl = models.TextField()
    #music_nice = models.IntegerField( default = 0 )
    
class LikeList( models.Model ):#いいね
    like_music_id = models.IntegerField()
    like_user_mail = models.EmailField()

class HistoryList( models.Model ):#履歴
    history_music_id = models.IntegerField()
    history_user_mail = models.EmailField()

class Comment( models.Model ):#コメント
    comment_id = models.AutoField( primary_key = True )
    comment_text = models.TextField()
    comment_user_mail = models.EmailField()
    comment_music_id = models.IntegerField()
    comment_good = models.IntegerField()
    comment_posted = models.DateTimeField( auto_now_add = True )

class Result( models.Model ):
    result_comment_id = models.IntegerField()
    result_text = models.TextField()
    result_user_mail = models.EmailField()
    result_music_id = models.IntegerField()
    result_posted = models.DateTimeField( auto_now_add = True )