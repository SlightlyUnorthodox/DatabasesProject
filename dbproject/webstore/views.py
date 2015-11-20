from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import *
#import necessary models
from .models import User, Order, Supplier, Contains, Product
from .forms import LoginForm, RegisterForm

@login_required(login_url='/login/')
def index(request):
	return HttpResponse("Welcome to [name of webstore here]'s index.")

#CSRF tokens not enfored in test environment
@csrf_exempt
def login_user(request):
	#logout(request)
	#try:
	#	state
	#except NameError:
	#state = "Please enter login information below"

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
				else:
					print("Log: password inccorect")
					state = "Your username and/or password were incorrect."
			else:
				print("Log: username does not exist")
				state = "Your account is not active, please contact the site admin."
	else:
		form = LoginForm()
			
	return render(request, 'auth.html',{'form':form})

#CSRF tokens not enforced in test environment
@csrf_exempt
def register_user(request):
	#try:
	#	state
	#except NameError:
	#	state = "Please enter registration information below"
	
	address = username = password = passwordCheck = email = ''
	
	if request.method == 'POST':
	
		form = RegisterForm(request.POST)
		
		if form.is_valid():

			newUsername = request.POST.get('username')
			newPassword = request.POST.get('password')
			newPasswordCheck = request.POST.get('repassword')
			newAddress = request.POST.get('address')
			newEmail = request.POST.get('email')

			print(newUsername)
			print(newPassword)
			print(newPasswordCheck)
			print(newAddress)
			print(newEmail)

			if newPassword != newPasswordCheck:
				state = "Your entered password does not match. Please re-enter"
				return render(request, 'register.html',{'form':form})

			# Attempt to add to database, check successful
			else:
				newUser = User(user_name = newUsername,user_password = newPassword,user_address = newAddress,user_email = newEmail)
				newUser.save()
				print("Log: new user successfully created")
				state = "New account created. Now login!"
				return render(request, 'auth.html',{'form':form})
		else:
			form = RegisterForm()
		
	state = "Please enter correct information"
	return render(request, 'register.html',{'form':form})
