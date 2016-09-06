# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_auto_20160826_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flat',
            name='user',
        ),
    ]
