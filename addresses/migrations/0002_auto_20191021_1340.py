# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-10-21 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(default='Santa Domingo', max_length=120),
        ),
    ]
