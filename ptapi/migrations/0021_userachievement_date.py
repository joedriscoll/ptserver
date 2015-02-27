# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0020_user_exercise_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userachievement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 27, 19, 14, 8, 951287), auto_now=True),
            preserve_default=False,
        ),
    ]
