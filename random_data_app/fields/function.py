from django.db import models


"""
Stores a single function that has a set of arguments
"""
class FunctionField(models.Field):
    description = "A Python Function"

    def __init__(self, *args, **kwargs):
        super(FunctionField, self).__init__(*args, **kwargs)


    def deconsruct(self):
        name, path, args, kwargs = super(FunctionField, self).deconsruct()
        return name, path, args, kwargs
