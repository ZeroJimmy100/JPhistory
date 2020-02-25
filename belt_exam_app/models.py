from django.db import models
from datetime import datetime, date
import re


class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(post_data["type_first_name"]) < 3:
            errors["first_name"] = 'First Name should be at least 3 characters or more'
        if len(post_data["type_last_name"]) < 2:
            errors["last_name"] = 'Last Name should be at least 3 characters or more'
        if not EMAIL_REGEX.match(post_data['type_email']):    # test whether a field matches the pattern      
            errors['email'] = "Invalid email address!"
        else:
            user_email = User.objects.filter(email= post_data['type_email'])
            if user_email:
                errors['email'] = "This email has already been used"
        if len(post_data["type_email"]) < 10:
            errors["email"] = 'Email should be at least 10 characters or more'
        if len(post_data["type_password"]) < 5:
            errors["password"] = 'Password should be at least 5 characters or more'
        if post_data["type_confirm"] != post_data["type_password"]:
            errors["password"] = "Confirm password must match your password you've created"
        return errors

class QuoteManager(models.Manager):
    def getValid(self, post_data):
        errors={}
        if len(post_data['quote_add']) < 3:
            errors["quote"] = 'Thought should be at least 3 characters or more'
        return errors

class CheckManager(models.Manager):
    def check_validator(self, post_data, request):
        errors = {}

        user_check = User.objects.get(id=request['user'])

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data["change_first"]) <= 0:
            errors["first_name"] = 'First Name should be at least 3 characters or more'
        if len(post_data["change_last"]) <= 0:
            errors["last_name"] = "Last Name should be at least 2 characters or more"
        if not EMAIL_REGEX.match(post_data['change_email']):
            errors['email'] = "Invalid Email"
        if user_check.email != post_data['change_email']: 
            user_email = User.objects.filter(email= post_data['change_email'])
            if user_email:
                errors['email'] = "This email has already been used"
        if len(post_data['change_email']) <= 0:
            errors['email'] = "Invalid Email"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    objects2 = CheckManager()

class Quote(models.Model):
    quote = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="quote_uploaded", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

class Likes(models.Model):
    related_quote = models.ForeignKey(Quote, related_name="my_likes", on_delete = models.CASCADE)
    get_like_user = models.ForeignKey(User, related_name="users", on_delete = models.CASCADE)
    mylike = models.IntegerField()

   
