from __future__ import unicode_literals
import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

import random
import string
from random_data_app.generators.image_generator import ImageSample
from django.utils import timezone
#from random_data_app.models.sample import Sample
#from random_data_app.generators import population
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

class CharFieldSample:
    def sample(self, size, field, spec):
        return "".join(random.choice(string.ascii_lowercase) for i in range(field.max_length))

class BooleanSample:
    def __init__(self):
        self.gen = None
    def genDis(self, resultingDistribution=[0.5,0.5], count=0):
        #ensure that the sum of each result occurs a certain
        #percent of time. This ensures the distribution and
        #is not a probability
        op_count = [0, 0]
        end_dist = [count*resultingDistribution[0], count*resultingDistribution[1]]
        remaining = count
        for i in range(count):
            r = False
            if op_count[0] == end_dist[0]:
                r = False
            elif op_count[1] == end_dist[1]:
                r = True
            else:
                r = bool(random.getrandbits(1))

            if r:
                op_count[0] = op_count[0] + 1
            else:
                op_count[1] = op_count[1] + 1
            yield r

    def sample(self, size, field, spec=None):
        choices = ChoiceDistribution.objects.filter(field=spec)
        if self.gen == None and spec==None:
            return bool(random.getrandbits(1))
        elif self.gen == None and spec != None and len(choices) > 0:
            print "GENNNNNNN"
            true_choice = choices.filter(value="TRUE")
            false_choice = choices.filter(value="FALSE")
            resultingDistribution = [0.0, 0.0]
            gen_dis = False
            if len(true_choice) > 0 and true_choice[0].ensure_distribution:
                resultingDistribution[0] = true_choice[0].distribution
                gen_dis = True
            if len(false_choice) > 0 and false_choice[0].ensure_distribution:
                resultingDistribution[1] = false_choice[0].distribution
                gen_dis = True
            if gen_dis:
                self.gen = self.genDis(resultingDistribution, size)

        r = False
        if self.gen != None:
            r = next(self.gen)
        else:
            r = bool(random.getrandbits(1))

        return r

class DateSample:
    def sample(self, size, field, spec):
        return timezone.now()

class DateTimeSample:
    def sample(self, size, field, spec):
        return timezone.now()


class FieldSample:
    def sample(self, size, field, spec):
        pass

default_samples = {
        "CharField":CharFieldSample,
        "BooleanField":BooleanSample,
        "DateField":DateSample,
        "DateTimeField":DateTimeSample,
        "ImageField":ImageSample,
        "FileField":ImageSample
}

class Population(models.Model):
    name = models.CharField(max_length=160, null=True, blank=True)
    model = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    size = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        s = super(Population, self).save(*args, **kwargs)
        #Generate Field Specifications

        PopulationGenerator(population=self).generate()
        return s

class PopulationMember(models.Model):
    population = models.ForeignKey(Population)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        print self
        s = super(PopulationMember, self).save(*args, **kwargs)

        return s

    def __str__(self):
        return str(self.content_object)

class ChoiceDistribution(models.Model):
    value = models.CharField(max_length=80)
    distribution = models.FloatField()
    ensure_distribution = models.BooleanField(default=False)
    random = models.BooleanField(default=True)
    field = models.ForeignKey('FieldSpec')

class FieldSpec(models.Model):
    field_type = models.CharField(max_length=80)
    field_name = models.CharField(max_length=80)
    random = models.BooleanField(default=True)
    choices = models.ManyToManyField(ChoiceDistribution, blank=True, null=True)
    population = models.ForeignKey(Population)

class Sample(models.Model):
    population = models.ForeignKey(Population)
    member = models.ManyToManyField(PopulationMember, blank=True)
    size = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        s = super(Sample, self).save(*args, **kwargs)
        if (self.member == None or len(self.member.all()) == 0):
            #generate
            m = PopulationMember.objects.filter(population=self.population)
            r = random.sample(range(self.population.size), self.size)
            mlist = []
            print s
            for i in r:
                self.member.add(m[i])
            self.save()

        return s

@receiver(m2m_changed, sender=Sample.member.through)
def update_members(*args, **kwargs):
    obj = kwargs['instance']
    if (kwargs['action'] == 'post_remove'):
        m = PopulationMember.objects.filter(population=obj.population)
        pk_set = kwargs.pop('pk_set', None)
        for pk in pk_set:
            mp = m.get(pk=pk)
            sf = len(obj.member.filter(pk=pk))
            if sf == 0:
                obj.member.add(mp)


class PopulationGenerator:
    def __init__(self, population):
        self.population = population
        self.model_class = self.population.model.model_class()

        self.population_size = self.population.size
        self.samples = {} #for generating population
        self.fields = {}

    def kwarg_value(self, fieldname, fieldtype, field):
        field_specs = FieldSpec.objects.filter(population=self.population, field_type=fieldtype, field_name=fieldname)
        if len(field_specs) == 0:
            field_specs = FieldSpec(population=self.population,field_type=fieldtype, field_name=fieldname, random=True)
            field_specs.save()

        if (hasattr(self.samples, fieldname)):
            return self.samples[fieldname].sample()
        else:
            if self.fields.get(fieldname, None) == None:
                self.fields[fieldname] = default_samples[fieldtype]()

            return self.fields[fieldname].sample(self.population.size, field, field_specs)

    def generate_kwargs(self):
        kwargs = {}
        for f in self.model_class._meta.get_fields():
            if not f.auto_created:
                kwargs[f.name] = self.kwarg_value(f.name, f.get_internal_type(), f)

        return kwargs
    def clear_members(self):
        for m in PopulationMember.objects.filter(population=self.population):
            m.content_object.delete()
            m.delete()


    def generate(self):
        self.clear_members()
        for p in range(self.population.size):
            ct = self.model_class
            #m = self.population.model.model_class()
            kwargs =  self.generate_kwargs()
            i = ct(**kwargs)
            i.save()

            pm = PopulationMember(population=self.population, content_object=i)
            pm.save()
            #self.population.append(i)


        npm = PopulationMember.objects.filter(population=self.population)
        return npm
    def sample_random(self):
        return

    def sample_unique(self, unique_count):
        r = random.sample(range(self.population.size), unique_count)
        s = PopulationMember.objects.filter(population=self.population)
        sample = Sample(population=self.population, size=unique_count)
        sample.save()
        for i in r:
            sample.member.add(s[i])
            sample.save()
            yield s[i].content_object

    def sample(self, unique_count=0):
        if (unique_count==0):
            return self.sample_random()
        else:
            return self.sample_unique()
