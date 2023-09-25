from django.contrib import admin
from cwmapp.models import Music, Comment, Reply, LikeList, HistoryList, CustomUser, Star, Good, Album, GoodComment, GoodCommentReply

# Register your models here.
#from cwmapp.models import User

admin.site.register( CustomUser )
admin.site.register( Music )
admin.site.register( Comment )
admin.site.register( Reply )
admin.site.register( LikeList )
admin.site.register( HistoryList )
admin.site.register( Star )
admin.site.register( Good )
admin.site.register( Album )
admin.site.register( GoodComment )
admin.site.register( GoodCommentReply )