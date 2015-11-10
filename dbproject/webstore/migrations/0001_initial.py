# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contains',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(serialize=False, primary_key=True)),
                ('order_date', models.DateField()),
                ('order_paid', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(serialize=False, primary_key=True)),
                ('product_name', models.CharField(max_length=50)),
                ('product_description', models.CharField(max_length=200)),
                ('product_price', models.IntegerField()),
                ('product_active', models.BooleanField(default=False)),
                ('product_stock_quantity', models.IntegerField()),
                ('contains', models.ForeignKey(to='webstore.Contains')),
                ('order', models.ForeignKey(to='webstore.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supplier_id', models.AutoField(serialize=False, primary_key=True)),
                ('supplier_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(serialize=False, primary_key=True)),
                ('user_name', models.CharField(max_length=50)),
                ('user_password', models.CharField(max_length=50)),
                ('user_address', models.CharField(max_length=50)),
                ('user_email', models.CharField(max_length=50)),
                ('user_is_staff', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='supplys',
            field=models.ForeignKey(to='webstore.Supplier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='orders',
            field=models.ForeignKey(to='webstore.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contains',
            name='products',
            field=models.ManyToManyField(to='webstore.Order', through='webstore.Product'),
            preserve_default=True,
        ),
    ]
