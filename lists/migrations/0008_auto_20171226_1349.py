# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 13:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0007_auto_20171226_1335'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
    ]
