# Generated by Django 4.2 on 2023-07-13 00:33

import django.contrib.auth.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cwmapp', '0002_customuser_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='userid',
            field=models.CharField(default=uuid.UUID('dc409f02-044f-495f-ba8a-2b19bc5227b5'), error_messages={'msg': 'fuck!'}, help_text='この名前は公開されません。', max_length=100, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='userid'),
        ),
    ]
