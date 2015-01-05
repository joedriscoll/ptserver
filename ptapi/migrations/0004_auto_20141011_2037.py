# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptapi', '0003_auto_20141011_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('data', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('data', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password_hash', models.CharField(max_length=200)),
                ('name', models.CharField(default=b'name', max_length=100)),
                ('email', models.CharField(default=b'eamil', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password_hash', models.CharField(max_length=200)),
                ('name', models.CharField(default=b'name', max_length=100)),
                ('email', models.CharField(default=b'eamil', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='patient',
            name='assigned_pt',
            field=models.ForeignKey(to='ptapi.PT'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pain',
            name='patient',
            field=models.ForeignKey(to='ptapi.Patient'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='patient',
            field=models.ForeignKey(to='ptapi.Patient'),
            preserve_default=True,
        ),
    ]
