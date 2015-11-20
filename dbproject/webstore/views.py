from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import *
#import necessary models
from .models import User, Order, Supplier, Contains, Product
from .forms import LoginForm, RegisterForm

loggedIn = False

@login_required(login_url='/login')
def index(request):
	return HttpResponse("Welcome to [name of webstore here]'s index.")

#@login_required(login_url='/login')
def browse(request):
	return HttpResponse("Webstore browsing page")

#@login_required(login_url='/login')
def account(request):
	return HttpResponse("Webstore user account page")

#CSRF tokens not enfored in test environment
@csrf_exempt
def login_user(request):
	
	username = password = ''
	if request.method == 'POST':

		form = LoginForm(request.POST)

		if form.is_valid():
			
			username = request.POST.get('username')
			password = request.POST.get('password')

			if User.objects.filter(user_name = username).exists():
				user = User.objects.get(user_name = username)

				if user.user_password == password:
					print("Log: successfully logged in")
					state = "You've logged in!"
					return render(request, 'index.html')
					#return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
				else:
					print("Log: password inccorect")
					state = "Your username and/or password were incorrect."
			else:
				print("Log: username does not exist")
				state = "Your account is not active, please contact the site admin."
	else:
		form = LoginForm()
	
	state = "Please enter login information"		
	return render(request, 'auth.html',{'form':form,'state':state})

#CSRF tokens not enforced in test environment
@csrf_exempt
def register_user(request):
	
	address = username = password = passwordCheck = email = ''
	
	if request.method == 'POST':
	
		form = RegisterForm(request.POST)
		
		if form.is_valid():

			newUsername = request.POST.get('username')
			
			if User.objects.filter(user_name = newUsername).exists():
				state = "Username already exists"
				print("Log: username already exists")
				return render(request, 'register.html',{'form':form,'state':state})
			
			newPassword = request.POST.get('password')
			newPasswordCheck = request.POST.get('repassword')
			newAddress = request.POST.get('address')
			newEmail = request.POST.get('email')

			if User.objects.filter(user_email = newEmail).exists():
				state = "Email already exists"
				print("Log: email already exists")
				return render(request, 'register.html',{'form':form,'state':state})
			
			if newPassword != newPasswordCheck:
				state = "Your entered password does not match. Please re-enter"
				return render(request, 'register.html',{'form':form,'state':state})

			# Attempt to add to database, check successful
			else:
				newUser = User(user_name = newUsername,user_password = newPassword,user_address = newAddress,user_email = newEmail)
				newUser.save()
				print("Log: new user successfully created")
				state = "New account created. Now login!"
				return render(request, 'auth.html',{'form':form,'state':state})
	else:
		form = RegisterForm()
		
	state = "Please enter registration information"
	return render(request, 'register.html',{'form':form,'state':state})
