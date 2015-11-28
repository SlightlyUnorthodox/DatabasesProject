# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('webstore', '0005_auto_20151119_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_name',
        ),
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(unique=True, max_length=50, validators=[django.core.validators.MinLengthValidator(8, b'Your username must contain at least 8 characters.')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_password',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(8, b'Your password must contain at least 8 characters.')]),
        ),
    ]
