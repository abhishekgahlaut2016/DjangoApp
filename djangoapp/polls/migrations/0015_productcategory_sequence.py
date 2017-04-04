# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_cart_register_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='sequence',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True),
        ),
    ]
