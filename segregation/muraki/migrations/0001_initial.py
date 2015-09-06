# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alloy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name=b"Alloy's name")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Interpolation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('a0', models.CharField(max_length=200, verbose_name=b'Lattice parameter')),
                ('ac', models.CharField(max_length=200, verbose_name=b"Conductions's hydrostatic deformation potential")),
                ('av', models.CharField(max_length=200, verbose_name=b"Valence's hydrostatic deformation potential")),
                ('b', models.CharField(max_length=200, verbose_name=b'Deformation potential for tetragonal distorion')),
                ('c11', models.CharField(max_length=200, verbose_name=b'Elastic constant')),
                ('c12', models.CharField(max_length=200, verbose_name=b'Elastic constant')),
                ('me', models.CharField(max_length=200, verbose_name=b'Electron effective mass')),
                ('mhh', models.CharField(max_length=200, null=True, verbose_name=b'Heavy-hole effective mass')),
                ('mlh', models.CharField(max_length=200, null=True, verbose_name=b'Light-hole effective mass')),
                ('eg2', models.CharField(max_length=200, verbose_name=b'Gap energy at 2 K')),
                ('eg77', models.CharField(max_length=200, verbose_name=b'Gap energy at 77 K')),
                ('eg300', models.CharField(max_length=200, verbose_name=b'Gap energy at 300 K')),
                ('alloy', models.ForeignKey(verbose_name=b'The related alloy', to='muraki.Alloy')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('a0', models.FloatField(verbose_name=b'Lattice parameter')),
                ('ac', models.FloatField(verbose_name=b"Conductions's hydrostatic deformation potential")),
                ('av', models.FloatField(verbose_name=b"Valence's hydrostatic deformation potential")),
                ('b', models.FloatField(verbose_name=b'Deformation potential for tetragonal distorion')),
                ('c11', models.FloatField(verbose_name=b'Elastic constant')),
                ('c12', models.FloatField(verbose_name=b'Elastic constant')),
                ('me', models.FloatField(verbose_name=b'Electron effective mass')),
                ('mhh', models.FloatField(null=True, verbose_name=b'Heavy-hole effective mass')),
                ('mlh', models.FloatField(null=True, verbose_name=b'Light-hole effective mass')),
                ('eg2', models.FloatField(verbose_name=b'Gap energy at 2 K')),
                ('eg77', models.FloatField(verbose_name=b'Gap energy at 77 K')),
                ('eg300', models.FloatField(verbose_name=b'Gap energy at 300 K')),
                ('alloy', models.ForeignKey(verbose_name=b'The related alloy', to='muraki.Alloy')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
