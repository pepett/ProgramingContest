from django.contrib import admin

# Register your models here.
from cwmapp.models import User, Music, LikeList, HistoryList, Comment, Result

admin.site.register( User )
admin.site.register( Music )
admin.site.register( LikeList )
admin.site.register( HistoryList )
admin.site.register( Comment )
admin.site.register( Result )