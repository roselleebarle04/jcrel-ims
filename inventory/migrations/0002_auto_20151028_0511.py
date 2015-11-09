# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('created',)},
        ),
        migrations.RenameField(
            model_name='item',
            old_name='sku',
            new_name='supplier_code',
        ),
        migrations.AddField(
            model_name='item',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(default=b'INACTIVE', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
