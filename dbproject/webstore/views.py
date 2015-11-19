from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import *

def index(request):
	return HttpResponse("Welcome to [name of webstore here]'s index.")

#CSRF tokens not enfored in test environment
@csrf_exempt
def login_user(request):
	state = "Please enter login information below"
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "You've logged in!"
			else:
				state = "Your username and/or password were incorrect."
		else:
			state = "Your account is not active, please contact the site admin."

	return render_to_response('auth.html',{'state':state, 'username': username})

#CSRF tokens not enforced in test environment
@csrf_exempt
def register_user(request):
	state = "Please enter registration information below"
	address = username = password = passwordCheck = email = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		passwordCheck = request.POST.get('please verify password')
		address = request.POST.get('address')
		email = request.POST.get('email')

		if password != passwordCheck:
			state = "Your entered password does not match. Please re-enter"
		# Attempt to add to database, check successful
		#else:
		#	success = 
			#if success: 
			#	state = "Your account has successfully been created"
			#else:
			#	state = "That username is already in use"
			#	state = "Some of your information is incorrect"

	return render_to_response('register.html',{'state':state,'username':username})