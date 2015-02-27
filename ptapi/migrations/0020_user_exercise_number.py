# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0019_exercise_link_to_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='exercise_number',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
