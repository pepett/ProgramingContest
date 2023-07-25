# Generated by Django 4.2 on 2023-07-24 15:45

import django.contrib.auth.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cwmapp', '0018_alter_customuser_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='userid',
            field=models.CharField(default=uuid.UUID('0bc26aa3-a114-428b-9672-7f9154232841'), error_messages={'msg': 'fuck!'}, help_text='この名前は公開されません。', max_length=100, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='userid'),
        ),
    ]
