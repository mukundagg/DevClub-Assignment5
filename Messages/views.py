from django.shortcuts import render, redirect
from django.http import *
from . import models as message_models
from Users import models as user_models

# Create your views here.
def load_message(request, uniquenum):
    ourmsgs = [];
    for i in message_models.Message.objects.all():
        if i.uniquemsgno == int(uniquenum):
            isCourseAnnouncement = False;
            for j in user_models.Course.objects.all():
                if i.toMsg == str(j.courseCode):
                    isCourseAnnouncement = True;
                    break;
            if i.fromMsg == str(request.user.entryNo) or i.toMsg == str(request.user.entryNo) or isCourseAnnouncement:
                lmno = i.uniquemsgno;
                if i:
                    ourmsgs.append(i);
                    j = i;
                    while j.nextMsg:
                        j = j.nextMsg;
                        ourmsgs.append(j);
                    lmno = j.uniquemsgno;
                return render(request, "message.html", {'fullmsg' : ourmsgs, 'lastmsgno' : lmno})
                break;
    return HttpResponse("Sorry you do not have permission to access this page.")

def reply_message(request):
    for i in message_models.Message.objects.all():
        if i.uniquemsgno == int(request.POST["lastmsg"]):
            newreply = message_models.Message(fromMsg = str(request.user.entryNo), toMsg = i.fromMsg, content = request.POST["msgcont"]);
            newreply.save();
            i.nextMsg = newreply;
            i.save();
            break;
    return redirect("/message/" + request.POST["firstmsg"]);

def load_user_messages(request):
    msglist, fullmsglist, lastmsgids, count = [], [], [], 0
    for i in request.user.messagelist.forumMessages.all():
        msglist.append(i);
        fullmsglist.append([]);
        fullmsglist[count].append(i);
        j = i;
        while j.nextMsg:
            j = j.nextMsg;
            fullmsglist[count].append(j);
        lastmsgids.append(j.uniquemsgno);
        count += 1;
    return render(request, "usermessages.html", {'allmessages' : fullmsglist, 'allmessages2' : zip(fullmsglist, lastmsgids)});

def send_user_messages(request):
    ourmsg = message_models.Message(fromMsg = str(request.user.entryNo), toMsg = request.POST["msgto"], content = request.POST["msgcont"])
    ourmsg.save();
    request.user.messagelist.forumMessages.add(ourmsg);
    for i in user_models.Student.objects.all():
        if i.entryNo == request.POST["msgto"]:
            i.messagelist.forumMessages.add(ourmsg);
            break;
    for i in user_models.Instructor.objects.all():
        if i.entryNo == request.POST["msgto"]:
            i.messagelist.forumMessages.add(ourmsg);
            break;
    return redirect("/messages");

def reply_message_users(request):
    for i in message_models.Message.objects.all():
        if i.uniquemsgno == int(request.POST["lastmsg"]):
            newreply = message_models.Message(fromMsg = str(request.user.entryNo), toMsg = i.fromMsg, content = request.POST["replycontent"]);
            newreply.save();
            i.nextMsg = newreply;
            i.save();
            break;
    return redirect("/messages");