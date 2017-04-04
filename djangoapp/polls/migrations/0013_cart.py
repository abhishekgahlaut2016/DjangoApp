# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20170308_0730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('quantity', models.DecimalField(max_digits=6, decimal_places=2)),
                ('product_id', models.ForeignKey(to='polls.ProductImage', null=True)),
            ],
        ),
    ]
