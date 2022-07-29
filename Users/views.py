from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from . import models as user_models
from Grades import models as grade_models
from Documents import models as doc_models
from Quizzes import models as quiz_models
from Messages import models as message_models
import os, re, math

# Authlogic
def register(request):
    return render(request, "register.html");

def make(request):
    if(request.method == "POST"):
        userobj = request.POST;
        if(userobj["inlineRadioOptions"] == "Student"):
            stdnt = user_models.Student.createStudent(entry = userobj["entryNo"], mail = userobj["email"], passw = userobj["password"], name = userobj["fullname"]);
            messages.error(request, 'Registered Succesfully');
            return redirect("../../../")
        elif(userobj["inlineRadioOptions"] == "Instructor"):
            instr = user_models.Instructor.createInstructor(entry = userobj["entryNo"], mail = userobj["email"], passw = userobj["password"], name = userobj["fullname"]);
            messages.error(request, 'Registered Succesfully');
            return redirect("../../../");
        else:
            messages.error(request, 'An error occurred while Signing up');
            return redirect("../../../");

def makecourse(request):
    if(request.method == "POST"):
        objs = request.POST;
        newcrs = user_models.Course.createCourse(code = objs["coursecode"], name = objs["coursename"], totstud = objs["total"], start = objs["start"], end = objs["end"], period = objs["options"], stdlist = objs.getlist("study"), instructlist = objs.getlist("instruct"), semstr = int(objs["semester"]));
        return redirect("../../allcourses");

def login(request):
    return render(request, "login.html");

def check(request):
    member = authenticate(entryNo=request.POST["entryNo"], password=request.POST["password"]);
    if member is not None:
        auth_login(request, member);
        return redirect("../../../index");
    else:
        messages.error(request, 'Invalid Credentials');
        return redirect("../");

def logout(request):
    auth_logout(request);
    return redirect("../login/");

def load_profile(request, entryNo):
    if entryNo == None:
        entryNo = request.user.entryNo;
    for i in user_models.Student.objects.all():
        if i.entryNo == entryNo:
            modobj = i;
            modobj.password = None;
            return render(request, "profile.html", {'userBody': modobj, 'allCourses': [i for i in user_models.Course.objects.all() if i.ismember(modobj)]})
    for i in user_models.Instructor.objects.all():
        if i.entryNo == entryNo:
            modobj = i;
            modobj.password = None;
            return render(request, "profile.html", {'userBody': modobj, 'allCourses': [i for i in user_models.Course.objects.all() if i.ismember(modobj)]})
    for i in user_models.Admin.objects.all():
        if i.entryNo == entryNo:
            modobj = i;
            modobj.password = None;
            return render(request, "profile.html", {'userBody': modobj})
    for i in user_models.Member.objects.all():
        if i.entryNo == entryNo:
            modobj = i;
            modobj.password = None;
            return render(request, "profile.html", {'userBody': modobj})
    return HttpResponse("Not Found");

def edit_profile(request):
    request.user.about=request.POST["newabout"];
    if(not len(request.FILES) == 0):
        # For writing the new profile photo to our media folder
        with open("media/" + str(request.FILES["newprofile"].name), "wb+") as dest:
            for chunk in request.FILES["newprofile"].chunks():
                dest.write(chunk);
        request.user.profilephoto = "media/" + str(request.FILES["newprofile"].name);
    request.user.save();
    return redirect(f'../{request.user.entryNo}');

def add_course_doc(request):
    for i in user_models.Course.objects.all():
        if str(i.courseCode) == request.POST["coursecode"]:
            if(not len(request.FILES) == 0):
                with open("media/media/documents/" + str(request.FILES["newcoursedoc"].name), "wb+") as dest:
                    for chunk in request.FILES["newcoursedoc"].chunks():
                        dest.write(chunk);
                docx = doc_models.Docs(name=request.FILES["newcoursedoc"].name, file=("media/media/documents/" + str(request.FILES["newcoursedoc"].name)));
                docx.save();
                i.save();
                i.documentsList.add(docx);
                break;
    return redirect(f'../{request.POST["coursecode"]}');


def load_course(request, courseCode):
    finalObj = None;
    for i in user_models.Course.objects.all():
        if i.courseCode == courseCode:
            finalObj = i;
            break; #        <!--{% if accessview %}-->
    thiscourseassignments = [];
    for i in request.user.allAssignments.all():
        if i.courseCode == courseCode:
            thiscourseassignments.append(i);        
    return render(request, "course.html", {'courseBody': finalObj, 'accessview': finalObj.ismember(request.user), 'allassignments': thiscourseassignments});

def add_course_assign(request):
    quizTrue = False;
    """if not request.POST.get("assignquiz", None):
        quizTrue = not quizTrue;"""
    fe = request.FILES.get("assigninstructupload", None);
    for i in user_models.Course.objects.all():
        if str(i.courseCode) == request.POST["coursecode"]:
            docx = None;
            if fe:
                with open("media/media/documents/" + str(request.FILES["assigninstructupload"].name), "wb+") as dest:
                    for chunk in fe.chunks():
                        dest.write(chunk);
                docx = doc_models.Docs(name=request.FILES["assigninstructupload"].name, file=("media/media/documents/" + str(request.FILES["assigninstructupload"].name)));
                docx.save();
                i.save();
            i.addAssignment(name = request.POST["assignname"], description = request.POST["assigndescription"], isQuiz = quizTrue, datedue = request.POST["endDate"], file = docx, quize = None, marks = request.POST["assignmarks"]);
            break;
    return redirect(f'../{request.POST["coursecode"]}');

def submit_course_assign(request):
    for i in request.user.allAssignments.all():
        if i.name == request.POST.get("assignmentcode"):
            i.notes = request.POST.get("yourresponse");
            fe = request.FILES.get("submitfile", None);
            docx = None;
            if fe:
                with open("media/media/documents/" + str(request.FILES["submitfile"].name), "wb+") as dest:
                    for chunk in fe.chunks():
                        dest.write(chunk);
                docx = doc_models.Docs(name=request.FILES["submitfile"].name, file=("media/media/documents/" + str(request.FILES["submitfile"].name)));
                docx.save();
            i.submission = docx;
            i.isSubmitted = True;
            i.save();
    return redirect(f'../{request.POST["coursecode"]}');


def add_course_quiz(request):
    ourquiz = quiz_models.Quiz(name = request.POST["quizname"], startdatetime = request.POST["quizstartdatetime"], enddatetime = request.POST["quizenddatetime"], duration = request.POST["quizduration"], instructions = request.POST["quizinstructions"], maxmarks = request.POST["quizmaxmarks"]);
    ourquiz.save();
    allpostitems = " ".join(str(i) for i in request.POST).split(" ")
    for i in range(0, len(allpostitems)):
        if allpostitems[i].startswith("secn"):
            secn = quiz_models.QuestionBank(name = str(allpostitems[i]));
            for j in range(i + 1, len(allpostitems)):
                if(allpostitems[j].startswith("secn")):
                    break;
                if(allpostitems[j].startswith("qn")):
                    qnNumb = int(allpostitems[j][2:])
                    qn = quiz_models.Question(qnNo = qnNumb, marks = int(request.POST[f"marksqn{qnNumb}"]), qnData = request.POST[f"qn{qnNumb}"]);
                    qn.save();
                    secn.save();
                    secn.listOfQns.add(qn);
                    secn.save();
            ourquiz.save();
            secn.save();
            ourquiz.listOfQnBanks.add(secn);
    ourquiz.save();

    for i in user_models.Course.objects.all():
        if str(i.courseCode) == request.POST["coursecode"]:
            ourquiz.save();
            i.save();
            validdateformat = request.POST["quizenddatetime"].index("T")
            i.addAssignment(name = ourquiz.name, description = "Quiz", isQuiz = True, datedue = request.POST["quizenddatetime"][0 : validdateformat], file = None, quize = ourquiz, marks = request.POST["quizmaxmarks"]);
            i.save();
            break;

    return redirect(f'../{request.POST["coursecode"]}');

def load_quiz(request, quizName):
    for i in request.user.allAssignments.all():
        if i.name == quizName and str(i.courseCode) == request.POST["coursecode"]:
            return render(request, "quiz.html", {'quizContents': i.quiz, 'isSubmitted' : i.isSubmitted, 'coursecode' : i.courseCode});
    return HttpResponse(quizName);

def submit_quiz(request):
    for i in request.user.allAssignments.all():
        if i.name == request.POST["quizname"] and str(i.courseCode) == request.POST["coursecode"]:
            count = 1;
            for j in i.quiz.listOfQnBanks.all():
                for k in j.listOfQns.all():
                    k.answer = request.POST["ans" + str(count)];
                    k.save();
                    count += 1;
                j.save();
            i.isSubmitted = True;
            i.save();
    return redirect(f'../course/{request.POST["coursecode"]}');

def add_quiz_marks(request):
    for i in user_models.Student.objects.all():
        if i.entryNo == request.POST["usrname"]:
            allearnt = 0;
            for j in i.allAssignments.all():
                if j.name == request.POST["assignname"]:
                    counter = 1;
                    for k in j.quiz.listOfQnBanks.all():
                        for m in k.listOfQns.all():
                            m.usrmarks = int(request.POST[f"eachqnmarks_{counter}"]);
                            counter += 1;
                            m.save();
                            allearnt += m.usrmarks;
                    j.save();
                    j.earntMarks = allearnt;
                    j.save();
            i.save();
    return redirect(f"/gradecourse/{request.POST['coursecode']}");

def grade_course(request, courseCode):
    thecourse = None;
    assignList, studList = [], [];
    for j in user_models.Course.objects.all():
        if j.courseCode == courseCode:
            thecourse = j;
    count = 0;
    for j in thecourse.studentList.all():
        studList.append(j);
        assignList.append([]);
        for i in j.allAssignments.all():
            if str(i.courseCode) == courseCode:
                assignList[count].append(i);
        count += 1;
    return render(request, "gradecourse.html", {'assignAll' : zip(studList, assignList), 'coursecode' : courseCode});

def submit_grades(request):
    ourlist = (" ".join(str(i) for i in request.POST)).split(" ")
    for i in ourlist:
        if(i.startswith("grade")):
            entryNum = i.split("_")[1];
            assignNo = int(i.split("_")[2]);
            for j in user_models.Member.objects.all():
                if j.entryNo == entryNum:
                    ourassign = j.allAssignments.all()[assignNo - 1];
                    if(request.POST.get(i, None) == '' or request.POST.get(i, None) == None):
                        ourassign.grade = '0';
                    else:
                        ourassign.grade = request.POST.get(i, None);
                    ourassign.save();
                    j.save();
                    break;
        elif(i.startswith("marks")):
            entryNum = i.split("_")[1];
            assignNo = int(i.split("_")[2]);
            for j in user_models.Member.objects.all():
                if j.entryNo == entryNum:
                    ourassign = j.allAssignments.all()[assignNo - 1];
                    if(not request.POST.get(i, None) or request.POST.get(i, None) == ''):
                        ourassign.earntMarks = 0;
                    else:
                        ourassign.earntMarks = int(request.POST.get(i, None));
                    ourassign.save();
                    j.save();
                    break;
    return redirect(f'../course/{request.POST["coursecode"]}');

def load_grades(request):
    courselist, gradelist = [], [];
    for i in user_models.Course.objects.all():
        for j in i.studentList.all():
            if str(j.entryNo) == str(request.user.entryNo):
                # Now we will calculate the grade, average
                grade, totalnum = 0.0, 0;
                for k in request.user.allAssignments.all():
                    if k.courseCode == i.courseCode:
                        earnmark, totmark = k.earntMarks, k.totalMarks
                        if(earnmark == 0 or earnmark == None):
                            earnmark = 0;
                        if(totmark == 0 or totmark == None):
                            continue;
                        grade += (int(earnmark) / totmark) * 10;
                        grd = k.grade;
                        if(grd == 'None' or grd == None or grd == ''):
                            grd = '0';
                        grade += int(grd);
                        totalnum += 1;
                if(totalnum == 0):
                    totalnum += 1;
                gradelist.append(round(grade / totalnum, 2));
                courselist.append(i);
                break;
    return render(request, "grades.html", {'ouruser': request.user, 'courselists' : zip(courselist, gradelist)});

def load_allcourses(request):
    courselist = [];
    for i in user_models.Course.objects.all():
        for j in i.studentList.all():
            if str(j.entryNo) == str(request.user.entryNo):
                courselist.append(i);
                break;
        for j in i.instructorList.all():
            if str(j.entryNo) == str(request.user.entryNo):
                courselist.append(i);
                break;
    return render(request, "courselists.html", {'allcourses' : courselist, 'allstudents': user_models.Student.objects.all(), 'allinstructors': user_models.Instructor.objects.all()})

def post_course_msg(request):
    for i in user_models.Course.objects.all():
        if str(i.courseCode) == request.POST["coursecode"]:
            newmsg = message_models.Message(title = request.POST["posttitle"], content = request.POST["msgcont"], fromMsg = str(request.user.entryNo), toMsg = request.POST["coursecode"]);
            newmsg.save();
            i.save();
            i.forum.forumMessages.add(newmsg);
            i.save();
            break;
    return redirect(f'../{request.POST["coursecode"]}');