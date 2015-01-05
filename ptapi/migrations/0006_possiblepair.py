# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0005_auto_20141011_2143'),
    ]

    operations = [
        migrations.CreateModel(
            name='PossiblePair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assigned_pt', models.ForeignKey(related_name=b'assigned_pt', to='ptapi.User')),
                ('patient', models.ForeignKey(to='ptapi.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
