from django.db import models
from Users import models as user_models
from django.utils import timezone

# Create your models here.
class Docs(models.Model):
    name = models.CharField(max_length=1000);
    #uploadedBy = models.ForeignKey(user_models.Instructor, on_delete=models.CASCADE, blank=True);
    uploadedBy = models.CharField(max_length=12, blank=True, default="None"); # entryNo for Students, Instructors
    file = models.FileField(upload_to = "media/documents/", max_length=1000);
    uploadedDate = models.DateTimeField(default=timezone.now);