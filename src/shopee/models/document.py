
from __future__ import unicode_literals

from django.db import models

class Document(models.Model):
    title = models.CharField(max_length = 200)
    uploadedFile = models.FileField(upload_to = "Uploaded Files/")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)
    # def __str__(self):
    #     return u"%s" % (self.title)
