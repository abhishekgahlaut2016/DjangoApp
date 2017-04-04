# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_productimage_product_thumbnail_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buyer_name', models.CharField(max_length=150)),
                ('buyer_email', models.CharField(max_length=150)),
                ('buyer_mobile', models.CharField(max_length=150)),
                ('buyer_address1', models.CharField(max_length=150)),
                ('buyer_address2', models.CharField(max_length=150)),
                ('buyer_pincode', models.CharField(max_length=150)),
                ('buyer_city', models.CharField(max_length=150)),
                ('buyer_state', models.CharField(max_length=150)),
                ('buyer_country', models.CharField(max_length=150)),
            ],
        ),
    ]
