# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_productimage_product_categ_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='product_thumbnail_image',
            field=models.ImageField(null=True, upload_to='polls/static/polls/thumb_images/', blank=True),
        ),
    ]
