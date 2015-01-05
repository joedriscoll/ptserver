# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0004_auto_20141011_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_pt', models.BooleanField(default=False)),
                ('password_hash', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('patient', models.ForeignKey(primary_key=True, serialize=False, to='ptapi.User')),
                ('assigned_pt', models.ForeignKey(related_name=b'assinged_pt', to='ptapi.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='patient',
            name='assigned_pt',
        ),
        migrations.DeleteModel(
            name='PT',
        ),
        migrations.AlterField(
            model_name='activity',
            name='patient',
            field=models.ForeignKey(to='ptapi.User'),
        ),
        migrations.AlterField(
            model_name='pain',
            name='patient',
            field=models.ForeignKey(to='ptapi.User'),
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
    ]
