# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_auto_20160826_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='user_fb_name',
            field=models.CharField(default=None, max_length=500, null=True, blank=True),
        ),
    ]
