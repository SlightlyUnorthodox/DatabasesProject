from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import *
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.db.models import Max
#import necessary models
from .models import User, Order, Supplier, Contains, Product
from .forms import LoginForm, RegisterForm, AccountActionForm, AccountUpdateForm, AccountDeleteForm
import datetime
import decimal

def index(request):
	template = loader.get_template('index.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def browse(request):

	product_list = Product.objects.order_by('product_id')
	price_sorted_product_list = Product.objects.order_by('product_price')
	template = loader.get_template('browse.html')
	context = RequestContext(request, {
		'product_list': product_list,
		'price_sorted_product_list': price_sorted_product_list,
		})
	return HttpResponse(template.render(context))

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

def order(request):
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	#going to need a list of products to choose from
	products = Product.objects.order_by('product_name')
	quantity = 0

	context = RequestContext(request)
	return render_to_response('order.html', {"products" : products, "quantity" : quantity}, context_instance=context)

def updateOrder(request):
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	productName = request.GET.get('productName')
	productExists = True
	try:
		productToAdd = Product.objects.get(product_name=str(productName))
	except:
		productExists = False

	#if there's a product to add, else just return
	if productExists:
		#If there's a product in the order
		if request.GET.get('productsInOrder'):
			#set to preexisting
			s = request.GET.get('productsInOrder')
			s = s.replace("'", "")
			productsInOrder = [e.encode('utf-8') for e in s.strip('[]').split(',')];

			

			s2 = request.GET.get('productsInOrderByID')
			s2 = s2.replace("'", "")
			productsInOrderByID = [e2.encode('utf-8') for e2 in s2.strip('[]').split(',')];

			#bug stop for none error initial none product value
			#not perfect, if 'None is in any product name, this will break'
			if 'None' in str(request.GET.get('productsInOrder')):
				productsInOrder = []
				productsInOrderByID = []
		else:
			#create
			# one will be added, create this values
			productsInOrder = []
			productsInOrderByID = []
	else:
		#if there's already a product in the order
		if not int(request.GET.get('quantity')) is 0:
			productsInOrder = None
			productsInOrderByID = None
		else:
			#set to preexisting
			s = request.GET.get('productsInOrder')
			s = s.replace("'", "")
			productsInOrder = [e.encode('utf-8') for e in s.strip('[]').split(',')];

			s2 = request.GET.get('productsInOrderByID')
			s2 = s2.replace("'", "")
			productsInOrderByID = [e2.encode('utf-8') for e2 in s2.strip('[]').split(',')]
	
			
	if productExists:
		#if order already has a product, add this new to the cost and list of products
		if int(request.GET.get('quantity')) is not 0:
			productsInOrder.append(str(productToAdd.product_name)) 
			quantity = int(request.GET.get('quantity')) + 1
			productsInOrderByID.append(str(productToAdd.product_id))
			price_of_order = int(request.GET.get('price_of_order')) + productToAdd.product_price;
			errorMessage = "Additional product added successfully"


		#if a product with that name exists, first order
		else:
			productsInOrder.append(str(productToAdd.product_name))
			quantity = 1
			productsInOrderByID.append(str(productToAdd.product_id))
			price_of_order = productToAdd.product_price
			errorMessage = "Product added successfully"
		#generate the cost based on the product, and order number
	else:
		#products there, noproductIDsInOrder to add, return same values
		if int(request.GET.get('quantity')) is not 0:
			price_of_order = request.GET.get('price_of_order')

			quantity = int(request.GET.get('quantity'))
			errorMessage = "No Product of name " + productName 

			#set to preexisting
			s = request.GET.get('productsInOrder')
			s = s.replace("'", "")
			productsInOrder = [e.encode('utf-8') for e in s.strip('[]').split(',')];

			s2 = request.GET.get('productsInOrderByID')
			s2 = s2.replace("'", "")
			productsInOrderByID = [e2.encode('utf-8') for e2 in s2.strip('[]').split(',')]
		# noproductIDsInOrder there, noproductIDsInOrder to add
		else: 
			productsInOrder = None
			productsInOrderByID = None
			price_of_order = 0
			quantity = 0
			errorMessage = "No Products in Order"

	#going to need to pass and parse this too
	productIDs = Product.objects.order_by('product_id')



	context = RequestContext(request)
	return render_to_response('order.html', {"quantity": quantity, "errorMessage": errorMessage, "productsInOrder": productsInOrder, "productsInOrderByID": productsInOrderByID, "price_of_order" : price_of_order}, context_instance=context)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def CreateProduct():

	return newProduct

def placeOrder(request):
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	

	#Gets those products from the order
	if request.GET.get('productsInOrderByID'):
		stringOfProductIDs = request.GET.get('productsInOrderByID')
		#array of products, parsed from list
		arrayOfProductIDs = stringOfProductIDs.replace("[", "").replace("]","")
		productIDsInOrder = []
		while "'" in arrayOfProductIDs:
			pIDinstance = find_between(arrayOfProductIDs, "'", "'")
			productIDsInOrder.append(Product.objects.get(product_id=pIDinstance))
			arrayOfProductIDs = arrayOfProductIDs.replace("'", "", 2);

	#create A new order, add it to 
	newOrder = Order()
	#max + 1 of all current orders
	dictObject = Order.objects.all().aggregate(Max('order_id'))
	maxID = dictObject['order_id__max']
	if not maxID:
		maxID = 0;
	newOrder.order_id = int(maxID) + 1
	newOrder.order_date = str(datetime.date.today())
	newOrder.order_paid = request.GET.get('price_of_order')
	newOrder.orders = User.objects.get(user_name=activeUser)

	quantity = int(request.GET.get('quantity'))
	

	orderContains = Contains.objects.create(quantity=quantity)
	orderContains.save()

	stringOfProductIDs = request.GET.get('productsInOrderByID')
	#array of products, parsed from list
	arrayOfProductIDs = stringOfProductIDs.replace("[", "").replace("]","")

	# goes through products. It works, at least for one of them
	#works for all but one
	while "'" in arrayOfProductIDs:
		pIDinstance = find_between(arrayOfProductIDs, "'", "'")
		orderProduct = Product.objects.get(product_id=pIDinstance)
		orderContains.productsLONGNAME.add(orderProduct)
		arrayOfProductIDs = arrayOfProductIDs.replace("'", "", 2);

	orderProduct.save()
	newOrder.contains = orderContains

	newOrder.save()	

 
 	orders = Order.objects.order_by('-order_date')
 	context = RequestContext(request)
	return render_to_response('orderPlaced.html', {"yourOrder" : newOrder, "productIDsInOrder" : productIDsInOrder, "orders" : orders, }, context_instance=context)#

def account(request,round = 0):
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
				render(request,"accountUpdate.html")
				return accountUpdate(request,0)
			if action == '2':
				print("Log: Delete account")
				render(request,"accountDelete.html")
				return accountDelete(request,0)
			if action == '3':
				print("Log: View orders")
				#return accountView(request)
	
	#Initialize account form on first cycle
	else:
		form = AccountActionForm()

	state = "Please select an account action"
	return render(request, 'account.html',{'form':form,'state':state})

#
# This is for Deleting items, HAS NOT BEEN TESTED	
#
def staffDeleteItems(request):
	####!!!!!!!!!!!!!!  Change below to require staff not just user
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	#get the items to change
	#product works, order works, user works
	try:
		int(request.GET.get('productIDtoChange'))
		productToChange = Product.objects.get(product_id=int(request.GET.get('productIDtoChange')))
		productToChange.delete()
	except ValueError:
		productToChange = None
	try:
		int(request.GET.get('orderIDtoChange'))
		orderToChange = Order.objects.get(order_id=int(request.GET.get('orderIDtoChange')))
		orderToChange.delete()
	except ValueError:
		orderToChange = None

	try:
		int(request.GET.get('userIDtoChange'))
		userToChange = User.objects.get(user_id=int(request.GET.get('userIDtoChange')))
		userToChange.delete()
	except ValueError:
		userToChange = None



	context = RequestContext(request)
	return render_to_response('staffUpdatesSaved.html', {}, context_instance=context)

def staffCreateItemsToAdd(request):
	####!!!!!!!!!!!!!!  Change below to require staff not just user
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)


	context = RequestContext(request)
	return render_to_response('staffCreateItemsToAdd.html', {}, context_instance=context)

def staffAddItems(request):
	#get the items to change
	#follows same format as saveUpdate, needs to be done after saveUpdate is completed
	#get the items to change
	
	try: 
		productToAdd = Product()
		productToAdd.product_id = str(request.GET.get('productToChangeID'))
		#update Product Values
		productToAdd.product_name = str(request.GET.get('productName'))
		productToAdd.product_description = str(request.GET.get('productDescription'))
		productToAdd.product_price = int(request.GET.get('productPrice'))
		integerOneorZero = int(request.GET.get('productActive'))
		booleanProductActive = False
		if integerOneorZero is 1:
			booleanProductActive = True
		productToAdd.product_active = booleanProductActive
		productToAdd.product_stock_quantity = int(request.GET.get('productStockQuantity'))
		productToAdd.supplies = str(request.GET.get('productSupplys'))


		#
		productToAdd.save()


	except ValueError:
		productToAdd = None
		errorMessage = "You did not fill out all the necessary components for product"
		return render_to_response('staffCreateItemsToAdd.html', {"errorMessage" : errorMessage}, context_instance=RequestContext(request))
	


	context = RequestContext(request)	
	return render_to_response('staffUpdate.html', {"allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=context)

def staffUpdate(request):
	####!!!!!!!!!!!!!!  Change below to require staff not just user
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	#going to need a list of products to choose from
	allProducts = Product.objects.order_by('product_id')
	allOrders = Order.objects.order_by('order_id')
	allUsers = User.objects.order_by('user_id')

	context = RequestContext(request)
	return render_to_response('staffUpdate.html', {"allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=context)

def staffUpdateItems(request):
	####!!!!!!!!!!!!!!  Change below to require staff not just user
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)

	#going to need a list of products to choose from
	allProducts = Product.objects.order_by('product_id')
	allOrders = Order.objects.order_by('order_id')
	allUsers = User.objects.order_by('user_id')

	#get the Items to change
	try:
		int(request.GET.get('productIDtoChange'))
		productToChange = allProducts.get(product_id=int(request.GET.get('productIDtoChange')))
	except ValueError:
		productToChange = None
	try:
		int(request.GET.get('orderIDtoChange'))
		orderToChange = allOrders.get(order_id=int(request.GET.get('orderIDtoChange')))
	except ValueError:
		orderToChange = None
	try:
		int(request.GET.get('userIDtoChange'))
		userToChange = allUsers.get(user_id=int(request.GET.get('userIDtoChange')))
	except ValueError:
		userToChange = None


	context = RequestContext(request)
	return render_to_response('staffUpdateItems.html', {"productToChange" : productToChange, "userToChange" : userToChange, "orderToChange" : orderToChange,"allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=context)

def staffSaveUpdates(request):
	####!!!!!!!!!!!!!!  Change below to require staff not just user
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)


	#get the items to change

	#need to change to try except and add error handling like in AddItems
	
	if request.GET.get('productToChangeID'):
		myID = str(request.GET.get('productToChangeID'))
		productToChange = Product.objects.get(product_id=myID)
		#update Product Values
		productToChange.product_name = str(request.GET.get('productName'))
		productToChange.product_description = str(request.GET.get('productDescription'))
		productToChange.product_price = int(request.GET.get('productPrice'))

		trueOrFalse = bool(request.GET.get('productActive'))
		productToChange.product_active = trueOrFalse
		productToChange.product_stock_quantity = int(request.GET.get('productStockQuantity'))
		productToChange.contains = str(request.GET.get('productContains'))
		productToChange.orders = str(request.GET.get('productOrders'))

		## so it doesn't break
		productToChange.supplies = Supplier.objects.get(supplier_name=str(request.GET.get('productSupplies')))
		
		#needs to be fixed

		#call isn't working for some reason???
		productToChange.save()


	else:
		productToChange = None
	if request.GET.get('orderToChangeID'):
		myID2 = str(request.GET.get('orderToChangeID'))
		orderToChange = Order.objects.get(order_id=myID)

		#update order values

		#needs to be fixed
		#orderToChange.order_paid = decimal(request.GET.get('orderPaid'))


		#below needs to be fixed
		#orderToChange.order_date = str(datetime.date(str(request.GET.get('orderDate'))))
			#needs to be fixed

		orderToChange.save()
	else:
		orderToChange = None
	if request.GET.get('userToChangeID'):
		myID3 = str(request.GET.get('userToChangeID'))
		userToChange = User.objects.get(user_id=myID3);

		#update user values
		userToChange.user_name = str(request.GET.get('userName'))
		userToChange.user_password = str(request.GET.get('userPassword'))
		userToChange.user_address = str(request.GET.get('userAddress'))
		userToChange.user_is_staff = str(request.GET.get('userIsStaff'))

		userToChange.save()

	else:
		userToChange = None



	context = RequestContext(request)
	return render_to_response('staffUpdatesSaved.html', {"productToChange" : productToChange, "userToChange" : userToChange, "orderToChange" : orderToChange}, context_instance=context)

def accountUpdate(request,round):
	#Require user login, if not redirect to login page
	try:
		activeUser = request.session['username']
	except KeyError:
		return login_user(request)
	print("0")
	#Check for POST request, if valid get action value
	if (request.method == 'POST') & (round > 0):
		form = AccountUpdateForm(request.POST)
		if form.is_valid():
			
			#Assign update attributes
			newPassword = request.POST.get('password')
			newPasswordCheck = request.POST.get('repassword')
			newAddress = request.POST.get('address')
			newEmail = request.POST.get('email')
			print("1")
			#Load user reference
			user = User.objects.get(user_name = activeUser)
			print(user.user_name)

			#If new email is assigned, checks for uniqueness, if not unique, report and cycle
			if User.objects.filter(user_email = newEmail).exists() & user.user_email != newEmail:
				print("2")
				state = "Email already exists"
				print("Log: email already exists")
				return render(request, 'accountUpdate.html',{'form':form,'state':state})
			
			#Checks password matching, if not, report and cycle
			if newPassword != newPasswordCheck:
				print("3")
				state = "Your entered password does not match. Please re-enter"
				return render(request, 'accountUpdate.html',{'form':form,'state':state})

			# Attempt to update database, check successful, if successful return to account page
			
			print("check check check")
			user.user_password = newPassword
			user.user_email = newEmail
			user.user_address = newAddress
			newUser.save()
			print("Log: new user successfully created")
			state = "Account successfully updated!"
			render(request,"account.html")
			return accountUpdate(request,0)

	#Initialize account form on first cycle
	else:
		print("0.25")
		form = AccountUpdateForm()
	print("1")
	state = "Enter updated account information"
	round = round + 1
	return render(request, "accountUpdate.html",{'form':form,'state':state})

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


#### Known bug list
#Contains relation in models.py --done

#update staffSaveUpdates to work for orders and users
#update staff addITems to work
#update staff deleteItems to work

#Sort by price on browse page
#general html updates
#on delete add to models.py
#testing adding, ordering, deleting, updating