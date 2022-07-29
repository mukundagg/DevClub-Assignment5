from django.contrib import admin
from .models import *

# Register your models here.
class QnImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploadedOn')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('qnNo', 'marks')

class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('name', 'summarks')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'startdatetime', 'enddatetime', 'maxmarks')

admin.site.register(QnImageModel, QnImageAdmin);
admin.site.register(Question, QuestionAdmin);
admin.site.register(QuestionBank, QuestionBankAdmin);
admin.site.register(Quiz, QuizAdmin);