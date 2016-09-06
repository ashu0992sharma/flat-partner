# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_auto_20160826_2156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flat',
            options={'verbose_name': 'flat', 'verbose_name_plural': 'flats'},
        ),
        migrations.AddField(
            model_name='flat',
            name='user_fb_id',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='flat',
            name='user',
            field=models.ForeignKey(to='mysite.User'),
        ),
    ]
