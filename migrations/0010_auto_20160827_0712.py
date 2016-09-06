# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0009_remove_flat_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flat',
            options={},
        ),
        migrations.AddField(
            model_name='flat',
            name='phone_number',
            field=models.CharField(default=None, max_length=12, null=True, blank=True),
        ),
    ]
