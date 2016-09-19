import base

class CharSample(base.Sample):
    def sample(self, size, field, spec):
        return timezone.now()
