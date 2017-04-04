# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='register_id',
            field=models.ForeignKey(blank=True, to='polls.Register', null=True),
        ),
    ]
