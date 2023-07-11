from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, BaseUserManager

import datetime


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
    music_star = models.IntegerField()#いらない
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
        return str( self.comment_id )

""" class Result( models.Model ):
    result_comment_id = models.IntegerField()
    result_user_mail = models.EmailField()
    result_text = models.TextField()
    result_posted = models.DateTimeField( auto_now_add = True )

    def __str__( self ):
        return self.result_text """

class Reply( models.Model ):
    reply_id = models.AutoField( primary_key = True )
    reply_comment_id = models.IntegerField()
    reply_user_mail = models.EmailField()
    reply_text = models.TextField()
    #reply_good = models.IntegerField()#返信のいいね
    reply_posted = models.DateTimeField( auto_now_add = True )

    def __str__( self ):
        return self.reply_user_mail

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

class Star( models.Model ):
    star_user_mail = models.EmailField()
    star_music_id = models.TextField()
    star_num = models.IntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint( fields=[ 'star_user_mail', 'star_music_id' ], name='unique_star' )
        ]

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
    '''userid = models.CharField(
        _( "userid" ),
        max_length=100,
        unique=True,
        help_text=_(
            "この名前は公開されません。"
        ),
        validators = [username_validator],
        error_messages={
            "msg": _( "fuck!" )
        }
    )'''
    image = models.ImageField( upload_to = 'images/' )
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