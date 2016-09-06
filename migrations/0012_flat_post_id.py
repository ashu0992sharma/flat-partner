# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0011_flat_furnishing_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='post_id',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
    ]