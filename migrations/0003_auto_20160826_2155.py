# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_flat_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flat',
            options={'verbose_name': 'flat', 'verbose_name_plural': 'Flats'},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
    ]
