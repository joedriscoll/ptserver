# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0011_exercise'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='reps',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
