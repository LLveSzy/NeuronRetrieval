# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_neuron_near_neuron_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='neuron',
            name='Archive_Name',
            field=models.CharField(default='', max_length=200, verbose_name='Archive_Name'),
        ),
        migrations.AddField(
            model_name='neuron',
            name='Development',
            field=models.CharField(default='', max_length=200, verbose_name='Development'),
        ),
        migrations.AddField(
            model_name='neuron',
            name='Original_Format',
            field=models.CharField(default='', max_length=200, verbose_name='Original_Format'),
        ),
        migrations.AddField(
            model_name='neuron',
            name='Primary_Brain_Region',
            field=models.CharField(default='', max_length=200, verbose_name='Primary_Brain_Region'),
        ),
        migrations.AddField(
            model_name='neuron',
            name='Primary_Cell_Class',
            field=models.CharField(default='', max_length=200, verbose_name='Primary_Cell_Class'),
        ),
        migrations.AddField(
            model_name='neuron',
            name='Secondary_Brain_Region',
            field=models.CharField(default='', max_length=200, verbose_name='Secondary_Brain_Region'),
        ),
        migrations.AddField(
            model_name='neuron',
            name='Secondary_Cell_Class',
            field=models.CharField(default='', max_length=200, verbose_name='Secondary_Cell_Class'),
        ),
        migrations.AddField(
            model_name='neuron',
            name='Species_Name',
            field=models.CharField(default='', max_length=200, verbose_name='Species_Name'),
        ),
        migrations.AddField(
            model_name='neuron',
            name='Tertiary_Brain_Region',
            field=models.CharField(default='', max_length=200, verbose_name='Tertiary_Brain_Region'),
        ),
        migrations.AddField(
            model_name='neuron',
            name='Tertiary_Cell_Class',
            field=models.CharField(default='', max_length=200, verbose_name='Tertiary_Cell_Class'),
        ),
    ]
