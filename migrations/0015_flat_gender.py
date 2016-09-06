# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0014_flat_like_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='gender',
            field=models.CharField(default=b'', max_length=1, blank=True, choices=[(b'M', b'Male'), (b'F', b'Female')]),
        ),
    ]
