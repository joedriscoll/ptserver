# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0018_auto_20150220_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='link_to_url',
            field=models.CharField(max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
