# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0008_auto_20150108_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='session_key',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
