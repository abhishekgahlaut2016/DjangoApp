# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-04 11:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_register_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.ImageField(default='/static/polls/images/background.gif', upload_to='/home/deepakn/djangoapp/polls/static/polls/images/')),
            ],
        ),
        migrations.AlterField(
            model_name='register',
            name='image',
            field=models.ImageField(default='/static/polls/images/background.gif', upload_to='/home/deepakn/djangoapp/polls/static/polls/images/'),
        ),
    ]