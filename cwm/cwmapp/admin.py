from django.contrib import admin
from cwmapp.models import User, Music, Comment, Result, LikeList, HistoryList

# Register your models here.
#from cwmapp.models import User

admin.site.register( User )
admin.site.register( Music )
admin.site.register( Comment )
admin.site.register( Result )
admin.site.register( LikeList )
admin.site.register( HistoryList )