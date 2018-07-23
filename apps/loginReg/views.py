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
        request.session['userid']=checkUser.id
        if checkUser:
            enteredpassword = request.POST['password'] 
            if (bcrypt.checkpw(enteredpassword.encode(),checkUser.password.encode())): 
                context = {
                    "allQuotes":Quote.objects.all()
                }
                return render(request,"loginReg/confirm.html",context)

def successLogin(request):
    context = {
        "allQuotes":Quote.objects.all()
    }
    return render(request,"loginReg/confirm.html",context)

def addQuote(request):
    if request.method=="POST":
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value,extra_tags="quote")
                return redirect('/addQuote')
        else:
            aUser=Register.objects.get(id=request.session['userid'])
            aQuote=Quote.objects.create(
                author=request.POST['author'],
                message=request.POST['quote'],
                uploader=aUser)
    return redirect("/quoteDisplay")

def showUserQuotes(request,num):
    editUser=Register.objects.get(id=num)
    context={
        "userQuotes": editUser.uploaded_quotes.all(),
        "username": editUser.first_name
    }
    return render(request, "loginReg/showUserQuotes.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request,num):
    a=Quote.objects.get(id=num)
    print("*"*25, a.message)
    a.delete()
    a.save()
    print("*"*25, a.message)
    return redirect("/quoteDisplay")

def edit(request,num):
    context={
        "upUser": Register.objects.get(id=num)
    }
    return render(request,"loginReg/editUser.html",context)

def updateUser(request,num):
    upUserNow= Register.objects.get(id=num)
    upUserNow.first_name = request.POST['first_name']
    upUserNow.last_name = request.POST['last_name']
    upUserNow.email = request.POST['email']
    upUserNow.save()
    return redirect('/quoteDisplay')
