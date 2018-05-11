# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-28 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uphone', models.CharField(max_length=11)),
                ('upass', models.CharField(max_length=18)),
                ('uname', models.CharField(default='匿名', max_length=30)),
                ('uemail', models.EmailField(max_length=254, null=True)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
    ]
