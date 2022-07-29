from django.contrib import admin
from .models import *

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseCode', 'coursePeriod', 'courseStart', 'courseEnd')

admin.site.register(Member);
admin.site.register(Student);
admin.site.register(Instructor);
admin.site.register(Admin);
admin.site.register(Course, CourseAdmin);