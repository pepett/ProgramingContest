from django.db import models

class User( models.Model ):#ユーザーのテーブル
    user_name = models.CharField( max_length = 50 )
    user_mail = models.EmailField( primary_key = True )
    user_pass = models.CharField( max_length = 50 )
    user_image = models.CharField( max_length = 200 )
    user_birthday = models.DateField( auto_now_add = True )

class Music( models.Model ):#曲のテーブル
    music_id = models.AutoField( primary_key = True )
    music_name = models.CharField( max_length = 100 )
    music_star = models.IntegerField( default = 0 )
    #music_nice = models.IntegerField( default = 0 )
    
class GoodList( models.Model ):#いいね
    good_music_id = models.IntegerField()
    good_user_mail = models.EmailField()

class HistoryList( models.Model ):#履歴
    history_music_id = models.IntegerField()
    history_user_mail = models.EmailField()

class Comment( models.Model ):#コメント
    comment_id = models.AutoField( primary_key = True )
    comment_text = models.TextField()
    comment_user_mail = models.EmailField()

class Result( models.Model ):
    result_comment_id = models.IntegerField()