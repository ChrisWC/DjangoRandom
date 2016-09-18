from django.test import TestCase

from random_data_app.models.population import Population, PopulationMember
from random_data_app.models.sample import Sample
from random_data_app.models.demo import Name
from random_data_app.generators.population import PopulationGenerator, Sample

from django.contrib.contenttypes.models import ContentType

class ModelTests(TestCase):
    def test_fields(self):
        print "TEST"

    def test_population(self):
        c =ContentType.objects.get(model=Name._meta.model_name)
        print c.model_class()
        pinst = Population(model=c, size=10)
        pinst.save()
        p = PopulationGenerator(pinst)
        p.population_size = 10
        p.generate()
        hist = [0]*p.population_size
        for i in p.sample_unique(10):
            hist[i.id-1] = hist[i.id-1] + 1
            self.assertEqual(hist[i.id-1], 1)

        s = Sample.objects.filter(population=p.population)[0]
        for i in s.member.all():
            hist[i.content_object.id-1] = hist[i.content_object.id-1] + 1
            self.assertEqual(hist[i.id-1], 2)
