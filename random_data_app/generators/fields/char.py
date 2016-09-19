import base

class CharSample(base.Sample):
    def __init__(self):
        super(CharSample, self).save(*args, **kwargs)

    def defaultRandom(self, size, field, spec):
        return "".join(random.choice(string.ascii_lowercase) for i in range(field.max_length))

    def sample(self, size, field, spec):
        res = None

        #res = super(CharSample, self).sample(size, field, spec)


        return defaultRandom(size, field, spec)
