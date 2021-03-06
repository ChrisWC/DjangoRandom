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
import re
import ast
class ForeignKeySample:
    gen = None
    def genDist(self, size, field, spec):
        p0 = '(?P<model>\w+)\((?P<args>\w+([=]\w+){0,1}([,]\s*\w+[=](\w+){0,1})*)\)'
        p1 = '(?P<key>[a-zA-Z0-9_]+)[=](?P<value>\w+)'
        choices = ChoiceDistribution.objects.filter(field=spec)

        if len(choices) == 0:
            yield None

        default_values = {

        }
        for choice in choices:
            r0 = re.search(p0, choice.value)
            if r0 != None:
                model_name = r0.group('model')
                arguments = r0.group('args')

                arg_list = arguments.split(',')
                filters = dict()
                for arg in arg_list:
                    kv = re.search(p1, arg)
                    if kv:
                        if kv.group('value').startswith("'") and kv.group('value').endswith("'"):
                            filters[kv.group('key')] = kv.group('value')[1:-1]
                        elif kv.group('value').lower() == 'true':
                            filters[kv.group('key')] = True
                        elif kv.group('value').lower() == 'false':
                            filters[kv.group('key')] = False
                        elif re.match("[-+]?\d+$",kv.group('value')) != None:
                            filters[kv.group('key')] = int(kv.group('value'))
                        elif re.match("[-+]?\d+[.]\d+$",kv.group('value')) != None:
                            filters[kv.group('key')] = float(kv.group('value'))


                if arg_list:
                    print len(arg_list)

                #toField = re.search('\w+', choice.value).group(0)
                dist = choice.distribution
                to_l = ContentType.objects.filter(model=model_name.lower())

                if len(to_l) > 0:
                    mclass = to_l[0].model_class()

                    o = mclass.objects.filter(**filters)
                    mx = len(o)
                    print o
                    if mx > 0:
                        for i in range(0, int(size*dist)):
                            yield o[random.randint(0, mx-1)]

    def sample(self, size, field, spec=None):
        #create a foreign key with with current model and specified model
        #the basic spec is 'modelname'
        self.gen = self.genDist(size, field, spec)
        try:
            return next(self.gen)
        except:
            self.gen = None

        return None

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
        "FileField":ImageSample,
        "ForeignKey":ForeignKeySample
}

class Population(models.Model):
    name = models.CharField(max_length=160, null=True, blank=True)
    #model = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #size = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        s = super(Population, self).save(*args, **kwargs)
        #Generate Field Specifications

        #PopulationGenerator(population=self).generate()
        return s

class PopulationMember(models.Model):
    population = models.ForeignKey(Population)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        s = super(PopulationMember, self).save(*args, **kwargs)

        return s

    def __str__(self):
        return str(self.content_object)


class Sample(models.Model):
    population = models.ForeignKey(Population)
    model = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    member = models.ManyToManyField(PopulationMember, blank=True)
    specs = models.ManyToManyField('FieldSpec', blank=True)
    size = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        s = super(Sample, self).save(*args, **kwargs)
        sg = SampleGenerator(self)
        sg.generate()
        sg.reflow()
        #if (self.member == None or len(self.member.all()) == 0):
            #generate
            #m = PopulationMember.objects.filter(population=self.population)
            #r = random.sample(range(self.size), self.size)
            #for i in r:
                #self.member.add(m[i])
            #self.save()
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

    def __str__(self):
        return self.field_name

class SampleGenerator:
    def __init__(self, sample):
        self.sample = sample
        self.model_class = self.sample.model.model_class()

        self.sample_size = self.sample.size
        self.samples = {} #for generating population
        self.fields = {}

    def kwarg_value(self, fieldname, fieldtype, field):
        field_specs = FieldSpec.objects.filter(field_type=fieldtype, field_name=fieldname)
        if len(field_specs) == 0:
            field_specs = FieldSpec(field_type=fieldtype, field_name=fieldname, random=True)
            field_specs.save()

        if (hasattr(self.samples, fieldname)):
            return self.samples[fieldname].sample()
        else:
            if self.fields.get(fieldname, None) == None:
                self.fields[fieldname] = default_samples[fieldtype]()

            return self.fields[fieldname].sample(self.sample.size, field, field_specs)

    def generate_kwargs(self):
        kwargs = {}
        for f in self.model_class._meta.get_fields():
            if not f.auto_created:
                kwargs[f.name] = self.kwarg_value(f.name, f.get_internal_type(), f)

        return kwargs
    def generate_relation_kwargs(self):
        kwargs = {}
        for f in self.model_class._meta.get_fields():
            if not f.auto_created and f.get_internal_type() in ['ForeignKey']:
                kwargs[f.name] = self.kwarg_value(f.name, f.get_internal_type(), f)

        return kwargs
    def clear_members(self):
        for m in PopulationMember.objects.filter(population=self.sample.population, content_type=self.sample.model):
            if m.content_object != None:
                m.content_object.delete()
            m.delete()


    def generate(self):
        self.clear_members()
        for p in range(self.sample.size):
            ct = self.model_class
            #m = self.population.model.model_class()
            kwargs =  self.generate_kwargs()
            i = ct(**kwargs)
            i.save()

            pm = PopulationMember(population=self.sample.population, content_object=i)
            pm.save()
            #self.population.append(i)

        npm = PopulationMember.objects.filter(population=self.sample.population, content_type=self.sample.model)
        return npm

    def reflow(self):
        #reflow relations for all members
        #get member objects
        pml = PopulationMember.objects.filter(population=self.sample.population, content_type=self.sample.model)
        for pm in pml:
            nk = self.generate_relation_kwargs()
            for key, value in nk.iteritems():
                pm.content_object.__dict__[key + "_id"] = value
                pm.content_object.save()
        return PopulationMember.objects.filter(population=self.sample.population, content_type=self.sample.model)

