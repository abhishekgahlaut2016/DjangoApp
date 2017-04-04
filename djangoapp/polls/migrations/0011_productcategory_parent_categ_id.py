# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_buyerdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='parent_categ_id',
            field=models.ForeignKey(to='polls.ProductCategory', null=True),
        ),
    ]
