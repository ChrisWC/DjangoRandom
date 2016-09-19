from fields import boolean, char, date, image, datetime, decimal, file, float

defaults = {
    "CharField":char.CharFieldSample,
    "BooleanField":boolean.BooleanSample,
    "DateField":date.DateSample,
    "DateTimeField":date.DateTimeSample,
    "ImageField":image.ImageSample,
    "FileField":file.FileSample
}

#if user does not define defaults
sample_fields = defaults
