from django.db import models
from django.utils import timezone
from Quizzes import models as quiz_models;
from Documents import models as doc_models;
from datetime import date
import importlib

# Create your models here.
class Assignment(models.Model):
    # dateCreated, dateDue, name, grade, student, gradedby, totalMarks, earntMarks, submissions
    name = models.CharField(max_length=500);
    description = models.CharField(max_length=50000, blank=True, default="No Description Provided");
    describeUpload = models.ForeignKey(doc_models.Docs, on_delete=models.CASCADE, null=True, blank=True);
    grade = models.CharField(max_length = 2, choices = [('0', 'No Grade'), ('13', 'X / Project, PHD. Contd.'), ('12', 'Z / Course Contd.'), ('11', 'S / Satisfactory'), ('10', 'A'), ('9', 'A-'), ('8', 'B'), ('7', 'B-'), ('6', 'C'), ('5', 'C-'), ('4', 'D'), ('3', 'D-'), ('2', 'E'), ('1', 'E-'), ('-6', 'F'), ('-1', 'NP / AUDIT PASS'), ('-2', 'NF / AUDIT FAIL'), ('-3', 'I / INCOMPLETE'), ('-4', 'W / WITHDRAWAL'), ('-5', 'U / UNSATISFACTORY')], default='0', null=True, blank=True);
    dateCreated = models.DateField(default=timezone.now);
    dateGraded = models.DateField(null=True,blank=True);
    dueDate = models.DateField(null=True,blank=True);
    totalMarks = models.IntegerField(null=True, blank=True);
    earntMarks = models.IntegerField(null=True, blank=True);
    submission = models.ForeignKey(doc_models.Docs, on_delete=models.CASCADE, null=True, blank=True, related_name="usersubmission");
    notes = models.CharField(max_length=3000, null=True, blank=True); # For the student
    remarks = models.CharField(max_length=3000, null=True, blank=True); # For the instructor
    quiz = models.ForeignKey(quiz_models.Quiz, on_delete=models.CASCADE, null=True, blank=True);
    isQuiz = models.BooleanField(default=False);
    isSubmitted = models.BooleanField(default=False);
    courseCode = models.CharField(max_length=6, default="CODE");

    @property
    def date_passed(self):
        if not self.dueDate:
            return False;
        return date.today() > self.dueDate

