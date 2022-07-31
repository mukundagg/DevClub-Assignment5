from Users import models as user_models;
from rest_framework import serializers

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user_models.Member;
        fields = ["entryNo", "fullname", "programme", "department", "year"]; 

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user_models.Course;
        fields = ["courseCode", "courseName", "studentList", "instructorList", "noOfStudents", "courseStart", "courseEnd"];