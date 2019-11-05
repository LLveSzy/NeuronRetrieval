# coding:utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
# Create your models here.


class Neuron(models.Model):
    id = models.IntegerField(verbose_name='id', unique=True, primary_key=True,)
    name = models.CharField(verbose_name='neuron_name',
                            max_length=80, default='',
                            null=False, blank=False)
    near_neuron_list = models.CharField(verbose_name='near_neuron_list', unique=False, blank=False,
                                        max_length=200, default="")
    neuron_image = models.ImageField(verbose_name='neuron_picture', upload_to='Pic',
                                     blank=True, null=True)
    Archive_Name = models.CharField(verbose_name='Archive_Name', unique=False, blank=False, max_length=200, default="")
    Species_Name = models.CharField(verbose_name='Species_Name', unique=False, blank=False, max_length=200, default="")
    Development = models.CharField(verbose_name='Development', unique=False, blank=False, max_length=200, default="")
    Primary_Brain_Region = models.CharField(verbose_name='Primary_Brain_Region', unique=False, blank=False,
                                            max_length=200, default="")
    Secondary_Brain_Region = models.CharField(verbose_name='Secondary_Brain_Region', unique=False, blank=False,
                                              max_length=200, default="")
    Tertiary_Brain_Region = models.CharField(verbose_name='Tertiary_Brain_Region', unique=False, blank=False,
                                             max_length=200, default="")
    Primary_Cell_Class = models.CharField(verbose_name='Primary_Cell_Class', unique=False, blank=False, max_length=200,
                                          default="")
    Secondary_Cell_Class = models.CharField(verbose_name='Secondary_Cell_Class', unique=False, blank=False,
                                            max_length=200, default="")
    Tertiary_Cell_Class = models.CharField(verbose_name='Tertiary_Cell_Class', unique=False, blank=False,
                                           max_length=200, default="")
    Original_Format = models.CharField(verbose_name='Original_Format', unique=False, blank=False,
                                       max_length=200, default="")


    class Meta:
        verbose_name = u'neuron_name'
        verbose_name_plural = u'neuron_name'

    def __str__(self):
        return self.name

# class Detail_Id(models.Model):
#     id = models.IntegerField(verbose_name='deatil_id', unique=False, primary_key=True, )
#
#     class Meta:
#         verbose_name = u'Detail_Id'
#         verbose_name_plural = u'Detail_Id'
#
#     def __str__(self):
#         return self.id


