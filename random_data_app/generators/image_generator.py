import numpy
import Image
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import StringIO
import os
import random
from random_data.settings import MEDIA_ROOT
from django.db import models
import uuid, os
def renameup(filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename#os.path.join('/', filename)

class ImageSample:
    def sample(self, size, field=None, spec=None):
        dim = [8,8]
        size = [400, 400]
        data = None

        dsize = [size[0]/dim[0], size[1]/dim[1]]
        #Create ian Image
        img = numpy.zeros([size[0], size[1], 3], dtype=numpy.uint8)
        img[:] = random.randint(5, 255)

        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        len0 = size[0]/8.0
        for j in range(dim[1]):
            for i in range(dim[0]):
                img[len0*i:len0*(i+1), len0*j:len0*(j+1), :] = random.choice([color , [255,255,255]])

        img_io = StringIO.StringIO()
        im = Image.fromarray(img)
        upload_to = ""
        if isinstance(field, models.ImageField):
            upload_to = field.upload_to
        else:
            upload_to = field['upload_to']
        fname =  renameup(filename="*.jpeg")
        filename = os.path.join(MEDIA_ROOT, upload_to,fname)
        local_file = os.path.join(upload_to, fname)
        im.save(filename, format='JPEG')
        return local_file
