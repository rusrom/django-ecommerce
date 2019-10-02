# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-10-02 10:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0003_cart_subtotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=120)),
                ('status', models.CharField(choices=[('new', 'New'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('shipped', 'Shipped'), ('closed', 'Closed'), ('refunded', 'Refunded')], default='new', max_length=20)),
                ('shipping_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
            ],
        ),
    ]
