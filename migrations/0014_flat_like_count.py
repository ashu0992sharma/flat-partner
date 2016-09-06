# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0013_flat_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='like_count',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
