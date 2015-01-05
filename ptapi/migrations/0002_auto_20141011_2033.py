# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='email',
            field=models.CharField(default=b'eamil', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pt',
            name='email',
            field=models.CharField(default=b'eamil', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(default=b'name', max_length=100),
        ),
        migrations.AlterField(
            model_name='pt',
            name='name',
            field=models.CharField(default=b'name', max_length=100),
        ),
    ]
