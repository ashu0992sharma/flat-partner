# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(default=None, max_length=50, null=True, blank=True)),
                ('state', models.CharField(default=None, max_length=50, null=True, blank=True)),
                ('country', models.CharField(default=None, max_length=50, null=True, blank=True)),
                ('formatted_address', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True)),
                ('price', models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True)),
                ('vacancy', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Flat',
                'verbose_name_plural': 'Flats',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('id', models.CharField(max_length=20, serialize=False, verbose_name='user id', primary_key=True)),
                ('first_name', models.CharField(default=b'', max_length=254, verbose_name='first name', blank=True)),
                ('middle_name', models.CharField(default=b'', max_length=254, verbose_name='middle name', blank=True)),
                ('last_name', models.CharField(default=b'', max_length=254, verbose_name='last_name name', blank=True)),
                ('username', models.CharField(unique=True, max_length=254, verbose_name='username')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True, verbose_name='phone_number', validators=[django.core.validators.RegexValidator(regex=b'[0-9]{10,12}', message="Phone number must be entered in the format: '9999999999'. Up to 12 digits allowed.")])),
                ('gender', models.CharField(default=b'', max_length=1, blank=True, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('dob', models.DateField(default=b'9999-01-01', verbose_name='dob', blank=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect it instead of deleting accounts.', verbose_name='active')),
                ('image', models.ImageField(max_length=700, null=True, upload_to=b'profile/image/', blank=True)),
                ('preferred_categories', django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True)),
                ('preferred_subcategories', django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True)),
                ('cms_access', models.BooleanField(default=False, help_text='Designates whether the user can log into CMS.', verbose_name='Has CMS access')),
                ('social_profiles', django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.AddField(
            model_name='flat',
            name='user',
            field=models.ForeignKey(related_name='favourites', to='mysite.User'),
        ),
    ]
