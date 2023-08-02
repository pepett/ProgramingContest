from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, BaseUserManager

from lib.utils import Utils
import datetime
import uuid
import random,string

'''class User( models.Model ):
    user_name = models.CharField( max_length = 50 )
    user_mail = models.EmailField( primary_key = True )
    user_pass = models.CharField( max_length = 30 )
    user_image = models.ImageField( upload_to = 'images/' )
    user_birthday = models.DateField()

    def __str__( self ):
        return self.user_mail'''

class UploadImage( models.Model ):#画像テーブル
    image = models.ImageField( upload_to = 'images/' )#一時的なイメージの建て替え

'''class Music( models.Model ):
    music_id = models.TextField( primary_key = True )
    music_star = models.IntegerField()#いらない
    music_ad = models.BooleanField()

    def __str__( self ):
        return self.music_id'''

class Comment( models.Model ):#コメントテーブル
    comment_id = models.AutoField( primary_key = True )#コメントのID
    #comment_user_mail = models.EmailField()#コメント下ユーザのメールアドレス
    comment_userid = models.CharField( max_length=100 )
    comment_music_id = models.TextField()#コメントされた音楽のID
    comment_text = models.TextField()#コメント本文
    comment_posted = models.DateTimeField( auto_now_add = True )#コメントした日時

    def __str__( self ):
        return str( self.comment_id )

""" class Result( models.Model ):
    result_comment_id = models.IntegerField()
    result_user_mail = models.EmailField()
    result_text = models.TextField()
    result_posted = models.DateTimeField( auto_now_add = True )

    def __str__( self ):
        return self.result_text """

class Reply( models.Model ):#返信テーブル
    reply_id = models.AutoField( primary_key = True )#返信のID
    reply_comment_id = models.IntegerField()#返信したコメントのID
    #reply_user_mail = models.EmailField()#返信したユーザのメールアドレス
    reply_userid = models.CharField( max_length=100 )
    reply_text = models.TextField()#返信本文
    reply_posted = models.DateTimeField( auto_now_add = True )#返信した日時

    def __str__( self ):
        return self.reply_userid

class LikeList( models.Model ):#いいねしたリストテーブル
    #like_user_mail = models.EmailField()#いいねしたユーザのメールアドレス
    like_userid = models.CharField( max_length=100 )
    like_music_id = models.TextField()#いいねした音楽のID

    def __str__( self ):
        return self.like_userid

class HistoryList( models.Model ):#履歴テーブル
    #history_user_mail = models.EmailField()#履歴のメールアドレス
    history_userid = models.CharField( max_length=100 )
    history_music_id = models.TextField()#履歴の音楽ID

    def __str__( self ):
        return self.history_userid

class Star( models.Model ):#評価テーブル
    #star_user_mail = models.EmailField()#評価したユーザのメールアドレス
    star_userid = models.CharField( max_length=100 )
    star_music_id = models.TextField()#評価した音楽のID
    star_num = models.IntegerField()#音楽に対する評価
    class Meta:#複合キー指定
        constraints = [
            models.UniqueConstraint( fields=[ 'star_userid', 'star_music_id' ], name='unique_star' )
        ]

class Good( models.Model ):#いいねテーブル
    #good_user_mail = models.EmailField()#いいねしたユーザのメールアドレス
    good_userid = models.CharField( max_length=100 )
    good_music_id = models.TextField()#いいねした音楽のID
    good_bool = models.BooleanField(default=False)#音楽に対するいいね
    class Meta:#複合キー指定
        constraints = [
            models.UniqueConstraint( fields=[ 'good_userid', 'good_music_id' ], name='unique_good' )
        ]

class Music( models.Model ):#ユーザが投稿した音楽テーブル
    def save_full_track( instance, filename ):#フルの楽曲を保存するパス
        ext = filename.split('.')[-1]
        return f'{ Album.objects.get( album_id = instance.music_album_id ).album_userid }/albums/{ instance.music_album_id }/tracks/full/{ instance.music_id }.{ ext }'
    def save_preview_track( instance, filename ):#プレビューの楽曲を保存するパス
        ext = filename.split('.')[-1]
        return f'{ Album.objects.get( album_id = instance.music_album_id ).album_userid }/albums/{ instance.music_album_id }/tracks/pre/{ instance.music_id }.{ ext }'
    music_id = models.TextField(default=Utils.randomid, primary_key = True )#曲のID
    music_album_id = models.TextField()#所属するアルバムのID
    music_name = models.CharField( max_length = 100 )
    music_track_full = models.FileField( upload_to = save_full_track )#フルの音楽
    music_track_preview = models.FileField( upload_to = save_preview_track )#プレビュー音楽
    #music_userid = models.TextField()#投稿者のID
    
class Album( models.Model ):#ユーザが投稿したアルバムテーブル
    def save_album_image( instance, filename ):
        ext = filename.split( '.' )[ -1 ]
        return f'{ instance.album_userid }/albums/{ instance.album_id }/image/{ instance.album_id }.{ ext }'
    album_id = models.TextField(default=Utils.randomid, primary_key = True )#アルバムのID
    album_userid = models.TextField()#投稿者のID
    album_name = models.CharField( max_length = 100 )
    album_image = models.FileField( upload_to = save_album_image )

class UserManager( BaseUserManager ):
    use_in_migrations = True
  
    def _create_user(self, email, password, **extra_fields):#userid, 
        """Create and save a user with the given username, email, and
        password."""
        #if not userid:
        #    raise ValueError('The given email must be set')
        if not email:
            raise ValueError( 'The given email must be set' )
        email = self.normalize_email(email)
  
        user = self.model(email=email, **extra_fields)#userid=userid, 
        user.set_password(password)
        user.save(using=self._db)
        return user
  
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        #extra_fields.setdefault( 'last_login', datetime.datetime.now( pytz.timezone('Asia/Tokyo') ) )
        return self._create_user(email, password, **extra_fields)
  
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
  
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
  
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    def save_user( instance, filename ):
        return f'{ instance.userid }/image/{ filename }'#ユーザ画像
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=50,
        help_text=_(
            "この名前は公開されます。"
        ),
        validators=[username_validator],
        error_messages={
            "msg": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), blank=True, primary_key=True)
    userid = models.CharField(
        _( "userid" ),
        max_length=100,
        unique=True,
        default=Utils.randomid,
        help_text=_(
            "この名前は公開されません。"
        ),
        validators = [username_validator],
        error_messages={
            "msg": _( "fuck!" )
        }
    )
    image = models.ImageField( upload_to = save_user )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        #abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username

    def mail_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    #def __str__( self ):
    #    return self.username