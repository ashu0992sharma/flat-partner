# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0010_auto_20160827_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='furnishing_type',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
    ]
