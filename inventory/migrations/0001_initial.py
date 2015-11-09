# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sku', models.CharField(max_length=200, null=True)),
                ('store_code', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('unit_cost', models.IntegerField(default=0)),
                ('brand', models.ForeignKey(to='inventory.Brand', null=True)),
                ('category', models.ForeignKey(to='inventory.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='item_model',
            field=models.ForeignKey(to='inventory.ItemModel', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='supplier',
            field=models.ForeignKey(to='inventory.Supplier', null=True),
        ),
    ]
