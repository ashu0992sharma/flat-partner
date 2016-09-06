# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_auto_20160826_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cms_access',
        ),
        migrations.RemoveField(
            model_name='user',
            name='preferred_categories',
        ),
        migrations.RemoveField(
            model_name='user',
            name='preferred_subcategories',
        ),
    ]
