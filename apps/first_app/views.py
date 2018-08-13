# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from .models import User, Class , Post , Reply
import bcrypt
# Create your views here.
def index(request):
	return render(request, "first_app/index.html")

def login(request):
	return render(request, "first_app/log_in.html")

def signup(request):
	return render(request, "first_app/sign_up.html")

def signups(request):
	if request.method == "POST":
		errors = User.objects.sign_up_validator(request.POST)
		if len(errors):
			for tag,value in errors.items():
				messages.error(request, value,extra_tags=tag)
				print(tag,value)
			return redirect('/login')
		else:
			if request.POST['position'] == "Educator":
				position = True
			else:
				position = False
			hash1 = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
			User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'],  email = request.POST['email'], password= hash1.decode('utf-8'), educator = position)
			print("Created User.")
			return redirect('/')
	else:
		return redirect("/signups")

def logins(request):
	if request.method == "POST":
		errors = User.objects.log_in_validator(request.POST)
		if len(errors):
			for tag,value in errors.items():
				messages.error(request, value,extra_tags=tag)
				print(tag,value)
			return redirect('/login')
		else:
			user = User.objects.get( email = request.POST['email'])
			request.session['user'] = user.id
			return redirect('/main')
	else:
		return redirect('/login')

def main(request):
	if request.session['user']:
		user = User.objects.get(id = request.session['user'])
		classes = Class.objects.all()
		context = {
			'user' : user,
			'classes': classes
		}
		return render(request, "first_app/main.html", context)
	else:
		return redirect("/")

def logout(request):
	del request.session['user']
	return redirect("/")

def create_class(request):
	if request.session['user']:
		return render(request, "first_app/create_class.html")
	else:
		return redirect("/")

def create_classes(request):
	if request.method == "POST":
		errors = Class.objects.create_class_validator(request.POST)
		if len(errors):
			for tag,value in errors.iteritems():
				messages.error(request, value,extra_tags=tag)
				print(tag,value)
			return redirect('/create_class')
		else:
			Class.objects.create(title = request.POST['title'], desc = request.POST['desc'], instructor = User.objects.get(id = request.session['user']))
			print("Created Class.")
			return redirect('/main')
	else:
		return redirect("/signups")

def signup_class(request, number):
	if request.session['user']:
		thisclass = Class.objects.get(id = number)
		context = {
			'class': thisclass
		}
		return render(request, "first_app/sign_up_class.html",context)
	else:
		return redirect('/')

def signup_classes(request, number):
	if request.method == "POST":
		user = User.objects.get(id = request.session['user'])
		thisclass = Class.objects.get(id = number)
		thisclass.students.add(user)
		thisclass.save()
		print("Register Complete")
		return redirect('/main')
	else:
		return redirect('/main')

def classroom(request, number):
	if request.session['user']:
		user = User.objects.get(id = request.session['user'])
		thisclass = Class.objects.get(id = number)
		context = {
			'user': user,
			'class': thisclass
		}
		if thisclass.instructor == user:
			return render(request, "first_app/class_main_admin.html", context)
		else:
			return render(request, "first_app/class_main.html", context)
	else:
		return redirect('/')

def post(request, number):
	if request.method == "POST":
		errors = Post.objects.post_validator(request.POST)
		if len(errors):
			print(errors)
			messages.error(request, errors)
			return redirect('/class/'+number)
		else:
			Post.objects.create(content = request.POST['content'], user = User.objects.get(id = request.session['user']), classs = Class.objects.get(id = number))
			print("Created Post.")
			return redirect('/class/'+number)
	else:
		return redirect('/main')

def dismiss(request, classnumber, studentnumber):
	thisclass = Class.objects.get(id = classnumber);
	student = User.objects.get(id = studentnumber);
	thisclass.students.remove(student)
	thisclass.save()
	return redirect('/class/'+classnumber)

def reply(request, classnumber, postnumber):
	if request.method == "POST":
		errors = Reply.objects.reply_validator(request.POST)
		if len(errors):
			messages.error(request, errors['content'])
			return redirect('/class/'+classnumber)
		else:
			Reply.objects.create(content = request.POST['content'], user = User.objects.get(id = request.session['user']), classs = Class.objects.get(id = classnumber), post = Post.objects.get(id = postnumber))
			print("Create Reply")
			return redirect('/class/'+classnumber)
	else:
		return redirect('/main')

