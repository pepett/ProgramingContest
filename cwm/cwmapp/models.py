from django.db import models

class User( models.Model ):
    user_name = models.CharField( max_length = 50 )
    user_mail = models.EmailField( primary_key=True )
    user_pass = models.CharField( max_length = 30 )
    user_image = models.ImageField( upload_to = 'images/' )
    user_birthday = models.DateTimeField()
