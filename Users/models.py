from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from Messages import models as message_models
import random
import importlib

# Create your models here.

class CustomMemberManager(BaseUserManager):
    """
        Custom user management model for our Students, Instructors and Admins
    """

    def create_user(self, entryNo, password, email, fullname, **extra_fields):  # Private constructor
        """
        :param entryNo: Every user has an unique entry number
        :param password: Hashed password only
        :param email: Must have email for official communication from LMS
        :param fullname: We must know their full name
        :param extra_fields: Rest are optional and can change from time to time
        :return: the created user object
        """
        if (not entryNo or not password or not email or not fullname):
            raise ValueError("Entry No., Fullname, E-Mail and Password must be set to create an user.");
        email = self.normalize_email(email);  # Convert to equivalent universal form
        user = self.model(entryNo=entryNo, email=email, fullname=fullname, **extra_fields);
        user.set_password(password);  # Django will hash and save it
        user.save();
        return user;

    def create_superuser(self, entryNo, password, email, fullname, **extra_fields):
        extra_fields.setdefault("is_staff", True);
        extra_fields.setdefault("is_superuser", True);
        extra_fields.setdefault("is_active", True);

        if (not (extra_fields.get("is_staff") or extra_fields.get("is_superuser") or extra_fields.get("is_active"))):
            raise ValueError("Admin must be set as True");
        return self.create_user(entryNo=entryNo, password=password, email=email, fullname=fullname, **extra_fields);


class Member(AbstractBaseUser, PermissionsMixin):
    entryNo = models.CharField(max_length=12, unique=True, blank=False);
    profilephoto = models.ImageField(upload_to="media/", default="static/profile.png");
    email = models.EmailField(max_length=500, unique=True, blank=False);
    password = models.CharField(max_length=500, blank=False);
    fullname = models.CharField(max_length=250, blank=False);
    about = models.CharField(max_length=1000, default="Edit profile to view.", blank=True);
    programme = models.CharField(max_length=7, choices=[('DUAL', 'DUAL (B.Tech + M.Tech)'), ('UG', 'Undergraduate'), ('PG', 'Post-Graduate'), ('PHD', 'PHD.'), ('STAFF', 'STAFF')], default='UG')
    
    assignModels = importlib.import_module("Grades.models");
    allAssignments = models.ManyToManyField(assignModels.Assignment, blank=True);

    department = models.CharField(max_length=20, choices=[('Computer Sci', 'Computer Science'), ('Maths', 'Maths'), ('Electrical', 'Electrical'), ('Mechanical', 'Mechanical'), ('Physics', 'Physics'), ('Textile', 'Textile'), ('Biotech', 'Biotech'), ('Applied Mechanics', 'Applied Mechanics')], default="Maths");
    year = models.IntegerField(default = 0);
    dateJoined = models.DateField(default=timezone.now);
    is_student = models.BooleanField(default=False);
    is_instructor = models.BooleanField(default=False);
    is_staff = models.BooleanField(default=True); # Should be able to login but has no other permissions
    is_superuser = models.BooleanField(default=False);
    is_active = models.BooleanField(default=True);  # If the user has deleted their account, simply set to 'False' rather than delete the user
    
    messagelist = models.ForeignKey(message_models.Forum, blank = True, null = True, on_delete=models.CASCADE);

    # Must set is_staff, is_superuser, is_active to True to become admin

    USERNAME_FIELD = 'entryNo';  # Set the username field to entry number only
    REQUIRED_FIELDS = ['email', 'password', 'fullname'];  # Certain Fields must be entered

    objects = CustomMemberManager();  # Specify all member objects of this class to be from the Member manager

    def list_students(self):
        return Member.objects.filter(is_student=True);

    def list_instructors(self):
        return Member.objects.filter(is_instructor=True);


class Student(Member):
    group = models.CharField(max_length=3, default="0");

    def __init__(self, *args, **kwargs):
        if not args:
            kwargs["is_student"] = True;
            newforum = message_models.Forum(name = kwargs["entryNo"]);
            newforum.save();
            kwargs["messagelist"] = newforum;
        super().__init__(*args, **kwargs);

    def createStudent(entry, mail, passw, name):
        Student.objects.create_user(entryNo = entry, password = passw, email = mail, fullname = name);

    def addToCourse(self, code : str):
        for i in Course.objects.all():
            if i.courseCode == code:
                i.studentList.add(self);
                return True;
        return False;



class Instructor(Member):
    def __init__(self, *args, **kwargs):
        if not args:
            kwargs["is_instructor"] = True;
            kwargs["programme"] = "STAFF";
            newforum = message_models.Forum(name = kwargs["entryNo"]);
            newforum.save();
            kwargs["messagelist"] = newforum;
        super().__init__(*args, **kwargs);

    def createInstructor(entry, mail, passw, name):
        Instructor.objects.create_user(entryNo = entry, password = passw, email = mail, fullname = name, programme="STAFF");

    def addToCourse(self, code : str):
        for i in Course.objects.all():
            if i.courseCode == code:
                i.instructorList.add(self);
                return True;
        return False;



class Admin(Instructor):
    is_superuser = True;



class Course(models.Model):
    courseCode = models.CharField(max_length=6);
    courseName = models.CharField(max_length=1000, default="None")
    coursephoto = models.ImageField(upload_to="media/", blank = True, null = True);
    coursebackground = models.ImageField(upload_to="media/", blank = True, null = True);
    studentList = models.ManyToManyField(Student, blank=True);
    instructorList = models.ManyToManyField(Instructor, blank=True);
    noOfStudents = models.IntegerField(blank=True);
    courseStart = models.DateField(blank=True);
    courseEnd = models.DateField(blank=True);
    coursePeriod = models.CharField(max_length=6, choices=[('SUMMER', 'SUMMER'), ('SPRING', 'SPRING'), ('FALL', 'FALL'),
                                                           ('WINTER', 'WINTER')], default='SUMMER')
    docmodels = importlib.import_module("Documents.models");
    documentsList = models.ManyToManyField(docmodels.Docs, blank=True);
    semester = models.IntegerField(default=1);
    forum = models.ForeignKey(message_models.Forum, blank = True, null = True, on_delete = models.CASCADE);

    def __init__(self, *args, **kwargs):
        if not args:
            kwargs["coursephoto"] = "static/courseprofile/" + str(random.randint(1, 6)) + ".jpg";
            kwargs["coursebackground"] = "static/coursebackground/" + str(random.randint(1, 6)) + ".jpg";
            newforum = message_models.Forum(name = kwargs["courseCode"]);
            newforum.save();
            kwargs["forum"] = newforum;
        super().__init__(*args, **kwargs);

    def getNoOfStudents(self):
        return Course.objects.all().count();

    def createCourse(code, name, stdlist, instructlist, totstud, start, end, period, semstr):
        cobj = Course.objects.create(courseCode = code, courseName = name, noOfStudents = totstud, courseStart = start, courseEnd = end, coursePeriod = period, semester = semstr);
        for i in stdlist:
            for j in Student.objects.all():
                if i == j.entryNo:
                    j.addToCourse(code);
        for i in instructlist:
            for j in Instructor.objects.all():
                if i == j.entryNo:
                    j.addToCourse(code);

    def ismember(self, objs : Member):
        for j in self.studentList.all():
            if objs.entryNo == j.entryNo:
                return True;
        for j in self.instructorList.all():
            if objs.entryNo == j.entryNo:
                return True;
        return False;

    def addAssignment(self, name, description, isQuiz, datedue, file = None, quize = None, marks = 0): # Each assignment for the course can be accesed from the individual student object
        code = self.courseCode;
        assignModels = importlib.import_module("Grades.models");
        for i in self.studentList.all():
            obj = assignModels.Assignment(name = name, description = description, isQuiz = isQuiz, courseCode = code, dueDate = datedue, quiz = quize, totalMarks = marks);
            if file:
                obj.describeUpload = file;
            obj.save();
            i.save();
            i.allAssignments.add(obj);
        for i in self.instructorList.all():
            obj = assignModels.Assignment(name = name, description = description, isQuiz = isQuiz, courseCode = code, dueDate = datedue, quiz = quize, totalMarks = marks);
            if file:
                obj.describeUpload = file;
            obj.save();
            i.save();
            i.allAssignments.add(obj);


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE); 
    course = models.ForeignKey(Course, on_delete=models.CASCADE);
    grade = models.CharField(max_length = 2, choices = [('0', 'No Grade'), ('13', 'X / Project, PHD. Contd.'), ('12', 'Z / Course Contd.'), ('11', 'S / Satisfactory'), ('10', 'A'), ('9', 'A-'), ('8', 'B'), ('7', 'B-'), ('6', 'C'), ('5', 'C-'), ('4', 'D'), ('3', 'D-'), ('2', 'E'), ('1', 'E-'), ('-6', 'F'), ('-1', 'NP / AUDIT PASS'), ('-2', 'NF / AUDIT FAIL'), ('-3', 'I / INCOMPLETE'), ('-4', 'W / WITHDRAWAL'), ('-5', 'U / UNSATISFACTORY')], default='No Grade');