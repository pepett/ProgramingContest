from django.db import models

class User( models.Model ):
    user_name = models.CharField( max_length = 50 )
    user_mail = models.CharField( max_length = 50, primary_key = True )
    user_pass = models.CharField( max_length = 50 )

class Music( models.Model ):
    music_name = models.CharField( max_length = 100 )
    music_eval = models.IntegerField( default = 0 )
    