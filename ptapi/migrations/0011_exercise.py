# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0010_auto_20150109_0214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days_assigned', models.CharField(max_length=7)),
                ('name', models.CharField(max_length=100)),
                ('lastFiveTimes', models.CharField(max_length=400)),
                ('patient', models.ForeignKey(to='ptapi.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
