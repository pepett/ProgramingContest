from django.db import models

class User( models.Model ):
    user_name = models.CharField( max_length = 50 )
    user_mail = models.EmailField( primary_key = True )
    user_pass = models.CharField( max_length = 30 )
    user_image = models.ImageField( upload_to = 'images/' )
    user_birthday = models.DateField()

    def __str__( self ):
        return self.user_mail

class UploadImage( models.Model ):
    image = models.ImageField( upload_to = 'images/' )
    
class Music( models.Model ):
    music_id = models.TextField( primary_key = True )
    music_star = models.IntegerField()
    music_ad = models.BooleanField()

    def __str__( self ):
        return self.music_id

class Comment( models.Model ):
    comment_id = models.AutoField( primary_key = True )
    comment_user_mail = models.EmailField()
    comment_music_id = models.TextField()
    comment_good = models.IntegerField()
    comment_text = models.TextField()
    comment_posted = models.DateTimeField( auto_now_add = True )

    def __str__( self ):
        return self.comment_user_mail

class Result( models.Model ):
    result_comment_id = models.IntegerField()
    result_user_mail = models.EmailField()
    result_text = models.TextField()
    result_posted = models.DateTimeField( auto_now_add = True )

    def __str__( self ):
        return self.result_text

class LikeList( models.Model ):
    like_user_mail = models.EmailField()
    like_music_id = models.TextField()

    def __str__( self ):
        return self.like_user_mail

class HistoryList( models.Model ):
    history_user_mail = models.EmailField()
    history_music_id = models.TextField()

    def __str__( self ):
        return self.history_user_mail