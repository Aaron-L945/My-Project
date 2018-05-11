# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-29 01:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('desc', models.TextField(null=True)),
                ('picture', models.ImageField(upload_to='static/upload/goodsType')),
            ],
        ),
    ]
