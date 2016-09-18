import random
import string
from image_generator import ImageSample
from django.utils import timezone
#from random_data_app.models.sample import Sample

from random_data_app.models.population import Population, PopulationMember
from django.contrib.contenttypes.models import ContentType

class CharFieldSample:
    def sample(self, field):
        return "".join(random.choice(string.ascii_lowercase) for i in range(field.max_length))

class BooleanSample:
    def sample(self, field):
        return bool(random.getrandbits(1))

class DateSample:
    def sample(self, field):
        return timezone.now()

class DateTimeSample:
    def sample(self, field):
        return timezone.now()


class FieldSample:
    def sample(self, field):
        pass

default_samples = {
        "CharField":CharFieldSample(),
        "BooleanField":BooleanSample(),
        "DateField":DateSample(),
        "DateTimeField":DateTimeSample(),
        "ImageField":ImageSample(),
        "FileField":ImageSample()
}

class PopulationGenerator:
    def __init__(self, population):
        #c = ContentType.objects.get(model=content_type._meta.model_name)
        #self.population_model = PopulationModel(model=c, size=population_size)
        #self.population_model.save()

        self.population = population
        self.model_class = self.population.model.model_class()

        #self.population_size = population_size
        self.samples = {} #for generating population

    def kwarg_value(self, fieldname, fieldtype, field):
        if (hasattr(self.samples, fieldname)):
            return self.samples[fieldname].sample()
        else:
            return default_samples[fieldtype].sample(field)

    def generate_kwargs(self):
        kwargs = {}
        for f in self.model_class._meta.get_fields():
            if not f.auto_created:
                kwargs[f.name] = self.kwarg_value(f.name, f.get_internal_type(), f)

        return kwargs

    def generate(self):
        for p in range(self.population_size):
            ct = self.model_class
            #m = self.population.model.model_class()
            kwargs =  self.generate_kwargs()
            i = ct(**kwargs)
            i.save()
            pm = PopulationMember(population=self.population, content_object=i)
            pm.save()
            #self.population.append(i)
        return PopulationMember.objects.filter(population=self.population)
"""
    def sample_random(self):
        return

    def sample_unique(self, unique_count):
        r = random.sample(range(self.population_size), unique_count)
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
"""
