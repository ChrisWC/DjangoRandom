from __future__ import unicode_literals
import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.db import models
from django.utils.safestring import mark_safe
from random_data.settings import MEDIA_ROOT
#from random_data_app.generators.image_generator import ImageSample
# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

import StringIO
#from random_data_app.generators.population import PopulationGenerator
class Name(models.Model):
    name = models.CharField(max_length=80)
    is_public = models.BooleanField()
    added = models.DateField()
    used = models.DateTimeField()
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    #population = GenericRelation('Population', related_query_name="name")

    def avatar_tag(self):
        return  mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.avatar))

    def save(self, *args, **kwargs):
        return super(Name, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name[:8])
