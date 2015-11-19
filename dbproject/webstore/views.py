from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import *
#import necessary models
from .models import User, Order, Supplier, Contains, Product

@login_required(login_url='/login/')
def index(request):
	return HttpResponse("Welcome to [name of webstore here]'s index.")

#CSRF tokens not enfored in test environment
@csrf_exempt
def login_user(request):
	logout(request)
	try:
		state
	except NameError:
		state = "Please enter login information below"

	username = password = ''
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "You've logged in!"
				return render(request, 'index.html')
			else:
				state = "Your username and/or password were incorrect."
		else:
			state = "Your account is not active, please contact the site admin."
			
	return render_to_response('auth.html',{'state':state, 'username': username})

#CSRF tokens not enforced in test environment
@csrf_exempt
def register_user(request):
	try:
		state
	except NameError:
		state = "Please enter registration information below"
	
	address = username = password = passwordCheck = email = ''
	if request.method == 'POST':
		print("yoyo")
		newUsername = request.POST.get('username')
		newPassword = request.POST.get('password')
		newPasswordCheck = request.POST.get('re-password')
		newAddress = request.POST.get('address')
		newEmail = request.POST.get('email')

		if password != passwordCheck:
			state = "Your entered password does not match. Please re-enter"
			return render_to_response('register.html',{'state':state,'username':username})

		# Attempt to add to database, check successful
		else:
			newUser = User(username = newUser,password =newPassword, address = newAddress,email = newEmail)
			newUser.save()
			return render_to_response('login.html',{'state':state,'username':username})
	state = "Please enter correct information"
	return render_to_response('register.html',{'state':state,'username':username})
