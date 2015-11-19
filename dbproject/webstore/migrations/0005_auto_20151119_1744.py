# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('webstore', '0004_auto_20151119_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(unique=True, max_length=50, validators=[django.core.validators.MinLengthValidator(8, b'Your username must contin at least 8 characters.')]),
        ),
    ]
