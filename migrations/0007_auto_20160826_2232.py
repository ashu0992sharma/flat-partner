# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_flat_user_fb_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='image',
            field=models.CharField(default=None, max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='flat',
            name='publish_at',
            field=models.DateTimeField(null=True, verbose_name='Post Publish Date', blank=True),
        ),
    ]
