from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import *
from django.views.generic import FormView
from django.core.urlresolvers import reverse
#import necessary models
from .models import User, Order, Supplier, Contains, Product
from .forms import LoginForm, RegisterForm, AccountActionForm, AccountUpdateForm, AccountDeleteForm

def index(request):
	template = loader.get_template('index.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

#@login_required(login_url='/login')
def browse(request):

	product_list = Product.objects.order_by('product_id')
	template = loader.get_template('browse.html')
	context = RequestContext(request, {
		'product_list': product_list,
		})
	return HttpResponse(template.render(context))

def checkLoggedIn(request):
	try:
		userAccount = request.session['username']
		return userAccount
	except KeyError:
		return render(request,"auth.html")

#@login_required(login_url='/login')	
def account(request):
	userAccount = checkLoggedIn(request)
	print(userAccount)
	if request.method == 'POST':
		form = AccountActionForm(request.POST)
		if form.is_valid():
			action = request.POST.get('action')
			if action == '1':
				print("Update account")
				accountUpdate(request)
			if action == '2':
				print("Delete account")
			if action == '3':
				print("View orders")
	else:
		form = AccountActionForm()

	#Initialize form, first pass
	state = "Please select an account action"
	return render(request, 'account.html',{'form':form,'state':state})

def accountUpdate(request):
	if request.method == 'POST':
		form = AccountUpdateForm(request.POST)
		if form.is_valid():
			
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
		form = AccountUpdateForm()

	#Initialize form, first pass
	state = "Enter update account information"
	return render(request, "accountUpdate.html",{'form':form,'state':state})

#CSRF tokens not enfored in test environment
@csrf_exempt
def login_user(request):
	#logout user
	try:
		del request.session['username']
	except KeyError:
		pass

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
					request.session['username'] = user.user_name
					HttpResponseRedirect('index.html')
					return render(request, 'index.html')
					#return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
				else:
					print("Log: password incorrect")
					state = "Your username and/or password were incorrect."
			else:
				print("Log: username does not exist")
				state = "Your account is not active, please contact the site admin."
	else:
		form = LoginForm()
	
	state = "Please enter login information"		
	return render(request, 'auth.html',{'form':form,'state':state})


#
# REGISTRATION VIEW
#

#CSRF tokens not enforced in test environment
@csrf_exempt
def register_user(request):
	#Initialize User model variables
	address = username = password = passwordCheck = email = ''
	
	#Check if POST request was made
	if request.method == 'POST':

		#Register and validate form
		form = RegisterForm(request.POST)
		if form.is_valid():

			#Set new username and confirm unique
			#If not unique, report and cycle form
			newUsername = request.POST.get('username')
			if User.objects.filter(user_name = newUsername).exists():
				state = "Username already exists"
				print("Log: username already exists")
				return render(request, 'register.html',{'form':form,'state':state})

			#Set remaining user attributes
			newPassword = request.POST.get('password')
			newPasswordCheck = request.POST.get('repassword')
			newAddress = request.POST.get('address')
			newEmail = request.POST.get('email')

			#Confirm email unique, if not, report and cycle form
			if User.objects.filter(user_email = newEmail).exists():
				state = "Email already exists"
				print("Log: email already exists")
				return render(request, 'register.html',{'form':form,'state':state})

			#Check password match, if not, report and cycle form			
			if newPassword != newPasswordCheck:
				state = "Your entered password does not match. Please re-enter"
				return render(request, 'register.html',{'form':form,'state':state})

			# Attempt to add to database, check successful
			# If successful, redirect to login page
			else:
				newUser = User(user_name = newUsername,user_password = newPassword,user_address = newAddress,user_email = newEmail)
				newUser.save()
				print("Log: new user successfully created")
				state = "New account created. Now login!"
				return render(request, 'auth.html',{'form':form,'state':state})
	else:
		#Initialize registration form
		form = RegisterForm()
		
	#Cycle initialized form		
	state = "Please enter registration information"
	return render(request, 'register.html',{'form':form,'state':state})
