"""DevClubLMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views as default_views
from Users import views as user_views
from Messages import views as message_views
from rest_framework import routers
from RestFramework import views as api_views

router = routers.DefaultRouter()
router.register(r'users', api_views.MemberViewSet);
router.register(r'courses', api_views.CourseViewSet);

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('forgot', default_views.forgotPass, name="forgot"),
    path('forgotten/<str:fern>', default_views.resetPass, name="reset"),
    path('approvedForgot', default_views.approvedPass, name="approvereset"),
    path('index/', default_views.index, name="index"),
    path('user/', include('Users.urls'), name="users"),
    path('message/<slug:uniquenum>', message_views.load_message, name="message"),
    path('messages/addreply', message_views.reply_message, name="reply"),
    path('messages/', message_views.load_user_messages, name="loadusermessage"),
    path('messages/newusermsg', message_views.send_user_messages, name="sendusermessage"),
    path('messages/replyusermsg', message_views.reply_message_users, name="replyusermessage"),
    path('grades/', user_views.load_grades, name="grades"),
    path('allcourses/', user_views.load_allcourses, name="allcourses"),
    path('quiz/<str:quizName>', user_views.load_quiz, name="quizzes"),
    path('submitquiz', user_views.submit_quiz),
    path('addquizmarks', user_views.add_quiz_marks),
    path('submitgrades', user_views.submit_grades),
    path('course/<slug:courseCode>', user_views.load_course, name="courses"),
    path('gradecourse/<slug:courseCode>', user_views.grade_course, name="gradecourses"),
    path('course/uploadcoursedocs/', user_views.add_course_doc, name="coursesdocs"),
    path('course/addassignment/', user_views.add_course_assign, name="coursesassign"),
    path('course/addquiz/', user_views.add_course_quiz, name="coursesquizadd"),
    path('course/postcourseforum/', user_views.post_course_msg, name="coursemsgpost"),
    path('course/submitassignment/', user_views.submit_course_assign, name="coursesassignsubmit"),
    path('', default_views.signin, name="signin"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT);
