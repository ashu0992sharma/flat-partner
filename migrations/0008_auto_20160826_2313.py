# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0007_auto_20160826_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='message',
            field=models.TextField(null=True, blank=True),
        ),
    ]
