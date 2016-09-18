from __future__ import unicode_literals
import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.db import models
from django.utils.safestring import mark_safe
from random_data.settings import MEDIA_ROOT
#from random_data_app.generators.image_generator import ImageSample
# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
"""
from random_data_app.models.population import Population, PopulationMember
class Sample(models.Model):
    population = models.ForeignKey(Population)
    member = models.ManyToManyField(PopulationMember)
    size = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        s = super(Sample, self).save(*args, **kwargs)

        return s
"""
