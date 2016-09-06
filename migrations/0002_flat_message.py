# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='message',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True),
        ),
    ]
