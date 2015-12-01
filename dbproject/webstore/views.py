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

#
# INDEX VIEW (basic html)
#

def index(request):
	template = loader.get_template('index.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

#
# BROWSE VIEW
#

def browse(request):

	product_list = Product.objects.order_by('product_id')
	price_sorted_product_list = Product.objects.order_by('product_price')
	template = loader.get_template('browse.html')
	context = RequestContext(request, {
		'product_list': product_list,
		'price_sorted_product_list': price_sorted_product_list,
		})
	return HttpResponse(template.render(context))

#
# Search attempt	
#

def search(request):
	query = request.GET.get('q')

	try:
		query = str(query)
	except ValueError:
		query = None
		results = None
	if query:
	   	results = Product.objects.order_by('product_name') # product name with str query in it
		results = results.filter(**{'product_name__icontains': str(query)}) #query, need to put in variable
		results_price_sorted = Product.objects.order_by('product_price') # product price
		results_price_sorted = results_price_sorted.filter(**{'product_name__icontains': str(query)}) 
	else:
		results = None
		results_price_sorted = None
	context = RequestContext(request)
	return render_to_response('browse.html', {"results" : results, "results_price_sorted": results_price_sorted}, context_instance=context)
#
# Order	
#
def order(request):
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	#going to need a list of products to choose from
	products = Product.objects.order_by('product_name')

	context = RequestContext(request)
	return render_to_response('order.html', {"products" : products}, context_instance=context)

#
# generates Cost and displays on page after updated with products added to order	
#
def updateOrder(request):
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	productName = request.GET.get('productName')
	truthCheck = True
	#If there's a product in the order
	if request.GET.get('productsInOrder'):
		#set to preexisting
		s = request.GET.get('productsInOrder')
		s = s.replace("'", "")
		productsInOrder = [e.encode('utf-8') for e in s.strip('[]').split(',')];
	else:
		#create
		productsInOrder = []

	try:
		productToAdd = Product.objects.get(product_name=str(productName))
	except:
		truthCheck = False
	if truthCheck:
		#if order already has a product, add this new to the cost and list of products
		if request.GET.get('price_of_order'):
			productsInOrder.append(str(productToAdd.product_name)) #this call is incorrect??
			price_of_order = int(request.GET.get('price_of_order')) + productToAdd.product_price;
			errorMessage = "Additional product added successfully"


		#if a product with that name exists, first order
		else:
			productsInOrder.append(str(productToAdd.product_name))
			price_of_order = productToAdd.product_price
			errorMessage = "Product added successfully"
		#generate the cost based on the product, and order number
	else:
		#products there, nothing to add, return same values
		if request.GET.get('price_of_order'):
			price_of_order = request.GET.get('price_of_order')
			errorMessage = "No Product of name " + productName 
		# nothing there, nothing to add
		else: 
			productsInOrder = None
			price_of_order = None
			errorMessage = "No Products in Order"

	context = RequestContext(request)
	return render_to_response('order.html', {"errorMessage": errorMessage, "productsInOrder": productsInOrder, "price_of_order" : price_of_order}, context_instance=context)
	

#
# Displays all orders in the system sorted by most recently placed???
#
def placeOrder(request):
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	count = 0
	if request.GET.get('productsInOrder'):
		for index in request.GET.get('productsInOrder'):
			count = count+1


	orders = Order.objects.order_by('order_date')
	context = RequestContext(request)
	return render_to_response('orderPlaced.html', {"orders" : orders, "numInOrder" : count}, context_instance=context)
#
# ACCOUNT VIEW (main)
#

def account(request):
	#Require user login, if not redirect to login page
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	#Check for POST request, if valid get action value
	if request.method == 'POST':
		form = AccountActionForm(request.POST)
		if form.is_valid():

			#Action value dictates which account page is rendered
			action = request.POST.get('action')
			if action == '1':
				print("Log: Update account")
				return accountUpdate(request)
			if action == '2':
				print("Log: Delete account")
				return accountDelete(request)
			if action == '3':
				print("Log: View orders")
				#return accountView(request)
	
	#Initialize account form on first cycle
	else:
		form = AccountActionForm()

	state = "Please select an account action"
	return render(request, 'account.html',{'form':form,'state':state})

#
# ACCOUNT UPDATE VIEW
#

def accountUpdate(request):
	#Require user login, if not redirect to login page
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	#Check for POST request, if valid get action value
	if request.method == 'POST':
		form = AccountUpdateForm(request.POST)
		if form.is_valid():
			
			#Assign update attributes
			newPassword = request.POST.get('password')
			newPasswordCheck = request.POST.get('repassword')
			newAddress = request.POST.get('address')
			newEmail = request.POST.get('email')

			#Load user reference
			user = User.objects.get(user_name = activeUser)
			print(user.user_name)

			#If new email is assigned, checks for uniqueness, if not unique, report and cycle
			if User.objects.filter(user_email = newEmail).exists() & user.user_email != newEmail:
				state = "Email already exists"
				print("Log: email already exists")
				return render(request, 'accountUpdate.html',{'form':form,'state':state})
			
			#Checks password matching, if not, report and cycle
			if newPassword != newPasswordCheck:
				state = "Your entered password does not match. Please re-enter"
				return render(request, 'accountUpdate.html',{'form':form,'state':state})

			# Attempt to update database, check successful, if successful return to account page
			else:
				user.user_password = newPassword
				user.user_email = newEmail
				user.user_address = newAddress
				newUser.save()
				print("Log: new user successfully created")
				state = "New account created. Now login!"
				return

	#Initialize account form on first cycle
	else:
		form = AccountUpdateForm()

	state = "Enter updated account information"
	return render(request, "accountUpdate.html",{'form':form,'state':state})

#
# ACCOUNT DELETE VIEW (incomplete)
#

def accountDelete(request):
	#Require user login, if not redirect to login page
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	#Check for POST request, if valid get action value
	if request.method == 'POST':
		form = AccountDeleteForm(request.POST)
		if form.is_valid():
			print("check0")
			#Assign update attributes
			confirm = request.POST.get('confirm')
			print("check1")
			#Load user reference
			user = User.objects.get(user_name = activeUser)
			print(user.user_name)
			print(user.email)
			print("check2")
			#If confirmatin successfully given, delete account
			#Report and log success, cycle back to main account page
			if confirm == user.user_email:
				state = "Account successfully deleted"
				print("Log: " + user.user_name + " account deleted")
				
				#Delete user
				User.objects.filter(user_name = activeUser).delete()

				return render(request, 'account.html',{'form':form,'state':state})
			
			#If confirmation unsuccessful, report and cycle page
			state = "Email confirmation incorrect"
			return render(request, 'accountDelete.html',{'form':form,'state':state})

	#Initialize account form on first cycle
	else:
		form = AccountDeleteForm()

	state = "Enter updated account information"
	return render(request, "accountDelete.html",{'form':form,'state':state})

#
# LOGIN VIEW
#

#CSRF tokens not enfored in test environment
@csrf_exempt
def login_user(request):
	#logout user from session
	try:
		del request.session['username']
	except KeyError:
		pass

	#initialize User model reference attributes
	username = password = ''

	#Check POST request and validate form
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			
			#Assign reference attributes
			username = request.POST.get('username')
			password = request.POST.get('password')

			#Confirm user name exists, if not state and cycle form
			if User.objects.filter(user_name = username).exists():
				user = User.objects.get(user_name = username)

				#Confirm password matches username
				#If so state success and redirect
				if user.user_password == password:
					print("Log: successfully logged in")
					state = "You've logged in!"
					request.session['username'] = user.user_name
					HttpResponseRedirect('index.html')
					return render(request, 'index.html')
				else:
				
					#If password doesn't match, report and cycle form
					print("Log: password incorrect")
					state = "Your username and/or password were incorrect."
					return render(request, "auth.html",{'form':form,'state':state})
			else:

				#If username does not exists, report and cycle form
				print("Log: username does not exist")
				state = "Your username and/or password were incorrect."
				return render(request, 'auth.html',{'form':form,'state':state})
	else:

		#Initialize login form
		form = LoginForm()
	
	#State and cycle rendering
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
