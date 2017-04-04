# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_productcategory_parent_categ_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='parent_categ_id',
            field=models.ForeignKey(blank=True, to='polls.ProductCategory', null=True),
        ),
    ]
