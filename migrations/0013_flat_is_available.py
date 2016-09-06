# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0012_flat_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
