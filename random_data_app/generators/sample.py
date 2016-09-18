import random
import string
from image_generator import ImageSample
from django.utils import timezone
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
