# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0012_exercise_reps'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='first_day',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 20, 2, 35, 16, 625396, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
