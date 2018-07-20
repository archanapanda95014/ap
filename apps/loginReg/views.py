from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request,"loginReg/index.html")

def register(request,method="POST"):
    errors = Register.objects.register_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request,value,extra_tags="register")
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        aUser=Register.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hash1)
        request.session['first_name']=aUser.first_name
        return redirect('/successLogin')

def login(request,method="POST"):
    errors = Register.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request,value,extra_tags="login")
        return redirect('/')
    else:
        checkUser=Register.objects.get(email=request.POST['email'])
        request.session['first_name']=checkUser.first_name
        if checkUser:
            enteredpassword = request.POST['password'] 
            if (bcrypt.checkpw(enteredpassword.encode(),checkUser.password.encode())):    
                return render(request,"loginReg/confirm.html")

def successLogin(request):
    return render(request,"loginReg/confirm.html")
