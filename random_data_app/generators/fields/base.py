class Sample(object):
    def __init__(self):
        self.generator = None

    def sample(self, size, field, spec):
        if self.generator:
            return next(self.generator)

        #create a generator
        pass
