# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('webstore', '0003_auto_20151119_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(unique=True, max_length=50, validators=[django.core.validators.MinLengthValidator]),
        ),
    ]
