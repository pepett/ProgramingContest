# Generated by Django 4.2 on 2023-09-27 20:57

import cwmapp.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import lib.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'msg': 'A user with that username already exists.'}, help_text='この名前は公開されます。', max_length=50, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, primary_key=True, serialize=False, verbose_name='email address')),
                ('userid', models.CharField(default=lib.utils.Utils.randomid, error_messages={'msg': 'fuck!'}, help_text='この名前は公開されません。', max_length=100, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='userid')),
                ('image', models.ImageField(upload_to=cwmapp.models.CustomUser.save_user)),
                ('is_premium', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', cwmapp.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('album_id', models.TextField(default=lib.utils.Utils.randomid, primary_key=True, serialize=False)),
                ('album_userid', models.TextField()),
                ('album_name', models.CharField(max_length=100)),
                ('album_image', models.FileField(upload_to=cwmapp.models.Album.save_album_image)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_userid', models.CharField(max_length=100)),
                ('comment_music_id', models.TextField()),
                ('comment_text', models.TextField()),
                ('comment_posted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good_userid', models.CharField(max_length=100)),
                ('good_music_id', models.TextField()),
                ('good_bool', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GoodComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gc_userid', models.CharField(max_length=25)),
                ('gc_comment_id', models.TextField()),
                ('gc_bool', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GoodCommentReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gcr_userid', models.CharField(max_length=25)),
                ('gcr_reply_id', models.TextField()),
                ('gcr_bool', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HistoryList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history_userid', models.CharField(max_length=100)),
                ('history_music_id', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LikeList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_userid', models.CharField(max_length=100)),
                ('like_music_id', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('music_id', models.TextField(default=lib.utils.Utils.randomid, primary_key=True, serialize=False)),
                ('music_album_id', models.TextField()),
                ('music_name', models.CharField(max_length=100)),
                ('music_track_full', models.FileField(upload_to=cwmapp.models.Music.save_full_track)),
                ('music_track_preview', models.FileField(upload_to=cwmapp.models.Music.save_preview_track)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('reply_id', models.AutoField(primary_key=True, serialize=False)),
                ('reply_comment_id', models.IntegerField()),
                ('reply_userid', models.CharField(max_length=100)),
                ('reply_text', models.TextField()),
                ('reply_posted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star_userid', models.CharField(max_length=100)),
                ('star_music_id', models.TextField()),
                ('star_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UploadImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.AddConstraint(
            model_name='star',
            constraint=models.UniqueConstraint(fields=('star_userid', 'star_music_id'), name='unique_star'),
        ),
        migrations.AddConstraint(
            model_name='goodcommentreply',
            constraint=models.UniqueConstraint(fields=('gcr_userid', 'gcr_reply_id'), name='unique_gcr'),
        ),
        migrations.AddConstraint(
            model_name='goodcomment',
            constraint=models.UniqueConstraint(fields=('gc_userid', 'gc_comment_id'), name='unique_gc'),
        ),
        migrations.AddConstraint(
            model_name='good',
            constraint=models.UniqueConstraint(fields=('good_userid', 'good_music_id'), name='unique_good'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
