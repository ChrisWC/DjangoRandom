
import base

class CharSample(base.Sample):
    def __init__(self):
        super(CharSample, self).save(*args, **kwargs)

    def nameGenerator(self, size, field, spec):
        return None

    def locationGenerator(self, size, field, spec):
        return None

    def sample(self, size, field, spec):
        res = None

        res = super(CharSample, self).sample(size, field, spec)
        return res
