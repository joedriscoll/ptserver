# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0002_auto_20141011_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='patient',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.RemoveField(
            model_name='pain',
            name='patient',
        ),
        migrations.DeleteModel(
            name='Pain',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='assigned_pt',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
        migrations.DeleteModel(
            name='PT',
        ),
    ]
