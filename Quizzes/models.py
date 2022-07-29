from django.db import models
from django.utils import timezone

# Create your models here.

class QnImageModel(models.Model):
    name = models.CharField(max_length=200);
    mainimage = models.ImageField(upload_to='qnimgs');
    uploadedOn = models.DateField(default=timezone.now);

class Question(models.Model):
    qnNo = models.IntegerField(blank = True, null = True);
    marks = models.IntegerField(blank = True, null = True);
    usrmarks = models.IntegerField(blank = True, null = True);
    qnData = models.CharField(max_length=10000, blank = True);
    qnFigures = models.ManyToManyField(QnImageModel, blank = True);
    answer = models.CharField(max_length=10000, blank = True);

class QuestionBank(models.Model):
    name = models.CharField(max_length=200, blank=True);
    listOfQns = models.ManyToManyField(Question, blank = True);
    instructions = models.CharField(max_length=10000, blank = True);
    summarks = models.IntegerField(blank = True, null = True);

class Quiz(models.Model):
    name = models.CharField(max_length=200, blank = True);
    startdatetime = models.DateTimeField(blank = True, default=timezone.now);
    enddatetime = models.DateTimeField(blank = True, default=timezone.now);
    duration = models.TimeField(blank = True);
    instructions = models.CharField(max_length=10000, blank = True);
    listOfQnBanks = models.ManyToManyField(QuestionBank, blank = True);
    maxmarks = models.IntegerField(blank = True, null = True);
    earntmarks = models.IntegerField(blank = True, null = True);

    @property
    def getduration(self):
        return str(self.duration);