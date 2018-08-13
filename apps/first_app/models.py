# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re
import bcrypt
# Create your models here.


class UserManager(models.Manager):
	def sign_up_validator(self, postData):
		errors = {}
		if len(postData['first_name']) < 2:
			errors["first_name"] = "Name should be at least 2 characters"
		elif not re.match('[A-Za-z]+', postData['first_name']):
			errors['first_name'] = "First name may only contain letters."
		if len(postData['first_name']) < 2:
			errors["first_name"] = "Name should be at least 2 characters"
		if len(postData['last_name']) < 2:
			errors["last_name"] = "First Name should be at least 2 characters"
		elif not re.match('[A-Za-z]+', postData['last_name']):
			errors['last_name'] = "Last name may only contain letters."
		elif not re.match('[A-Za-z]+', postData['first_name']):
			errors['name'] = "First name may only contain letters."
		if len(postData['password']) < 1:
			errors['email'] = "Please enter your email."
		elif User.objects.filter(email=postData['email']):
			errors['email'] = "Email is already taken."
		elif not re.match('[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+)*@[A-Za-z0-9-]+(.[A-Za-z0-9]+)*(.[A-Za-z]{2,})',postData['email']):
			errors['email'] = "Incorrect Email Format."
		if len(postData['password']) < 8:
			errors['password']= "Password must be longer than 8 characters"
		elif postData['pw_confirm'] != postData['password'] :
			errors['password']= "Password is not match"
		return errors
	def log_in_validator(self, postData):
		errors = {}
		if len(postData['email']) < 1:
			errors['email'] = "Please Enter Your Email"
		elif not re.match('[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+)*@[A-Za-z0-9-]+(.[A-Za-z0-9]+)*(.[A-Za-z]{2,})',postData['email']):
			errors['email'] = "Please Enter a Proper Email Address"
		elif not User.objects.filter(email = postData['email']):
			errors['email_not_found'] = "Your email and password does not match."
		if len(postData['password']) < 1:
			errors['password'] = "Please enter your password"
		elif not bcrypt.checkpw(postData['password'].encode('utf-8'), User.objects.get(email=postData['email']).password.encode('utf-8')):
			errors['password'] = "Please enter the correct email or password."
		return errors

class PostManager(models.Manager):
	def post_validator(self, postData):
		errors = {}
		if len(postData['content']) < 1:
			errors = "You cannot post a blank string."
		return errors


class ClassManager(models.Manager):
	def create_class_validator(self, postData):
		errors = {}
		if len(postData['title']) < 1:
			errors['title'] = "Please enter a proper class title."
		if len(postData['desc']) < 10:
			errors['desc'] = "Please enter a proper class desc"
		return errors

class ReplyManager(models.Manager):
	def reply_validator(self,postData):
		errors = {}
		if len(postData['content']) <1:
			errors['content'] = "Reply cannot be blank."
		return errors

class User(models.Model):
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	email = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)
	educator = models.BooleanField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Class(models.Model):
	title = models.CharField(max_length = 100)
	desc = models.TextField(max_length = 500)
	instructor = models.ForeignKey(User,on_delete= "DO_NOTHING", related_name="teach_classes")
	students = models.ManyToManyField(User,related_name="take_classes")
	objects = ClassManager()

class Post(models.Model):
	content = models.TextField(max_length = 500)
	user = models.ForeignKey(User, on_delete= "DO_NOTHING",related_name = "posts")
	classs = models.ForeignKey(Class, on_delete= "DO_NOTHING",related_name = "posts")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = PostManager()

class Reply(models.Model):
	content = models.TextField(max_length = 500)
	user = models.ForeignKey(User,on_delete= "DO_NOTHING", related_name = "replys")
	post = models.ForeignKey(Post,on_delete= "DO_NOTHING", related_name = "replys")
	classs = models.ForeignKey(Class,on_delete= "DO_NOTHING", related_name = "replys")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = ReplyManager()
