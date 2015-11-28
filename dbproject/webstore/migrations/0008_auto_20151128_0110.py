# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webstore', '0007_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='order',
            new_name='orders',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='supplys',
            new_name='supplies',
        ),
        migrations.AddField(
            model_name='product',
            name='product_name',
            field=models.CharField(default=b'Error: Bad product reference', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_paid',
            field=models.DecimalField(max_digits=19, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
