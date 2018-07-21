from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

class RegisterManager(models.Manager):
    def register_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name cannot be less than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name cannot be less than 2 characters"
        if len(postData['email']) < 1:
            errors["email"] = "email cannot be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors["valEmail"]="email should have @ and ."
        if len(postData['password']) < 1:
            errors["password"] = "password cannot be blank"
        if len(postData['confirmpassword']) < 1:
            errors["confirmpassword"] = "confirm password cannot be blank"
        elif postData['password'] != postData['confirmpassword']:
            errors['passwordmismatch'] = "password & confirm password should be the same"
        return errors

    def login_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['email']) < 1:
            errors["email"] = "email cannot be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors["valEmail"]="email should have @ and ."
        if len(postData['password']) < 1:
            errors["password"] = "password cannot be blank"
        enteredpswd = postData['password']
        checkUserA = Register.objects.filter(email=postData['email'])
        if not checkUserA:
            errors["invalidlogin"] = "Your login is invalid"           
        elif not (bcrypt.checkpw(enteredpswd.encode(),checkUserA[0].password.encode())):            
            errors["invalidpassword"] = "Your login is invalid"
        return errors

class Register(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegisterManager()
