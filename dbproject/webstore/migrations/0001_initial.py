# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


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
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(serialize=False, primary_key=True)),
                ('order_date', models.DateField()),
                ('order_paid', models.DecimalField(max_digits=19, decimal_places=2)),
                ('contains', models.ForeignKey(blank=True, to='webstore.Contains', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(serialize=False, primary_key=True)),
                ('product_description', models.CharField(max_length=200)),
                ('product_price', models.IntegerField()),
                ('product_active', models.BooleanField(default=False)),
                ('product_stock_quantity', models.IntegerField()),
                ('product_name', models.CharField(default=b'Error: Bad product reference', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supplier_id', models.AutoField(serialize=False, primary_key=True)),
                ('supplier_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(serialize=False, primary_key=True)),
                ('user_password', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(8, b'Your password must contain at least 8 characters.')])),
                ('user_address', models.CharField(max_length=50)),
                ('user_email', models.CharField(max_length=50)),
                ('user_is_staff', models.BooleanField(default=False)),
                ('user_name', models.CharField(unique=True, max_length=50, validators=[django.core.validators.MinLengthValidator(8, b'Your username must contain at least 8 characters.')])),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='supplies',
            field=models.ForeignKey(to='webstore.Supplier'),
        ),
        migrations.AddField(
            model_name='order',
            name='orders',
            field=models.ForeignKey(to='webstore.User'),
        ),
        migrations.AddField(
            model_name='contains',
            name='productsLONGNAME',
            field=models.ManyToManyField(to='webstore.Product'),
        ),
    ]
