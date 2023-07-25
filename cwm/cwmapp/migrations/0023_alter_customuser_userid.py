# Generated by Django 4.2 on 2023-07-25 00:56

import django.contrib.auth.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cwmapp', '0022_delete_commentgood_alter_customuser_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='userid',
            field=models.CharField(default=uuid.UUID('c2a3c7c6-e9fa-40bc-ac71-d1070ad13611'), error_messages={'msg': 'fuck!'}, help_text='この名前は公開されません。', max_length=100, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='userid'),
        ),
    ]
