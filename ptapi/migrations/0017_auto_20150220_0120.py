# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0016_user_session_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='days_assigned',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
