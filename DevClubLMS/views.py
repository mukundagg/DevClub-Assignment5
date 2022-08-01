from django.shortcuts import render, redirect
from http.client import HTTPResponse
from django.contrib import messages
from django.http import *
from Users import models as user_models
from cryptography.fernet import Fernet
from redmail import outlook
from django.contrib.auth.hashers import make_password

def index(request):
    return redirect(f"/user/{request.user.entryNo}");#render(request, "index.html", {'allstudents': user_models.Student.objects.all(), 'allinstructors': user_models.Instructor.objects.all()});

def signin(request):
    if request.user.is_authenticated:
        return redirect("index/");
    else:
        return redirect("user/login/");

def forgotPass(request):
    entrynum = request.POST["passReset"];
    email = None;
    for i in user_models.Student.objects.all():
        if i.entryNo == entrynum:
            email = i.email;
    for i in user_models.Instructor.objects.all():
        if i.entryNo == entrynum:
            email = i.email;
    if email:
        key = Fernet.generate_key();
        fernet = Fernet(key)
        fernnum = fernet.encrypt(entrynum.encode());
        try:
            outlook.username = user_models.Member.objects.get(entryNo="NOREPLYHOLO", is_superuser=True).email;
            outlook.password = user_models.Member.objects.get(entryNo="NOREPLYHOLO", is_superuser=True).password;

            outlook.send(
                receivers=[email],
                subject="Reset your HoloLMS Password",
                text=f"Please reset your password using the following link - https://hololms.herokuapp.com/forgotten/{fernnum.decode('utf-8')}"
            )

            ourmodel = user_models.PasswordModel(entryNo = entrynum, fernetNo = key.decode("utf-8"));
            ourmodel.save();
            messages.error(request, 'Please check your mail to reset your password.');
            return redirect("/"); 
        except Exception as ex:
            return HttpResponse(ex); 
        return HttpResponse("ok");

def resetPass(request, fern):
    return render(request, "verify.html", {"fern": fern});

def approvedPass(request):
    encMsg = request.POST["fern"];
    for i in user_models.PasswordModel.objects.all():
        fernet = Fernet(i.fernetNo);
        if i.entryNo == fernet.decrypt(bytes(encMsg, "utf-8")).decode():
            for j in user_models.Student.objects.all():
                if j.entryNo == i.entryNo:
                    j.password = make_password(request.POST["newpass"],hasher='default');
                    j.save();
                    i.delete();
                    messages.error(request, 'Your password has been succesfully reset');
                    return redirect("/");
                    break;
            for j in user_models.Instructor.objects.all():
                if j.entryNo == i.entryNo:
                    j.password = make_password(request.POST["newpass"],hasher='default');
                    j.save();
                    i.delete();
                    messages.error(request, 'Your password has been succesfully reset');
                    return redirect("/");
                    break;
    messages.error(request, 'An error occurred while resetting your password. Please contact the administrator.');
    return redirect("/");