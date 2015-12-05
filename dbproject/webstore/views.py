from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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
		#'price_sorted_product_list': price_sorted_product_list,
		})
	return HttpResponse(template.render(context))

def search(request):
	query = request.GET.get('q')
	price = request.GET.get('sort')
	
	try:
		query = str(query)
	except ValueError:
		query = None
		results = None

	if query:
	   	if price == None:
	   		results = Product.objects.order_by('product_name') # product name with str query in it
			results = results.filter(**{'product_name__icontains': str(query)}) #query, need to put in variable
			#results_price_sorted = None
			print("1")
		else:
			results = Product.objects.order_by('product_price') # product price
			results = results.filter(**{'product_name__icontains': str(query)}) 
			#results = None
			print("2")
	else:
		results = None
		results = None
	context = RequestContext(request)
	return render_to_response('browse.html', {"results" : results}, context_instance=context)

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

	stringOfProductIDs = request.GET.get('productsInOrderByID')
	#array of products, parsed from list
	arrayOfProductIDs = stringOfProductIDs.replace("[", "").replace("]","")

	# goes through products. It works, at least for one of them
	#works for all but one
	while "'" in arrayOfProductIDs:
		pIDinstance = find_between(arrayOfProductIDs, "'", "'")
		orderProduct = Product.objects.get(product_id=pIDinstance)
		productCount = orderProduct.product_stock_quantity
		# Decrement product quantity and check for low stock
		#productCount = orderProduct.get_field('product_stock_quantity')
		print("producCount: " + str(productCount))
		print("quantity: " + str(quantity))
		if quantity > productCount:
			print("Log: Error: no overselling allowed")
			state ="Insufficient product stock, please wait for staff to restock"
			return render(request,"order.html",{"state":state})
		elif productCount < 10:
			# Send severe warning to staff 
			print("Log: severe warning")
		elif productCount < 100:
			# Send warning to staff
			print("Log: minor warning")

		#orderProduct = Product(product_id = int(pIDinstance),product_stock_quantity = int(productCount - 1))
		

		#Product.objects.filter(product_id=pIDinstance).update(product_stock_quantity = productCount - 1)
		orderProduct.product_stock_quantity = (productCount -1)
		orderProduct.save()
		print(Product.objects.get(product_id=pIDinstance).product_stock_quantity)

		orderContains.productsLONGNAME.add(orderProduct)
		arrayOfProductIDs = arrayOfProductIDs.replace("'", "", 2);

		orderProduct.save()

	orderContains.save()

	newOrder.contains = orderContains

	newOrder.save()	

 
 	orders = Order.objects.order_by('-order_date').filter(orders__user_name__in = activeUser)
 	context = RequestContext(request)
	return render_to_response('orderPlaced.html', {"yourOrder" : newOrder, "productIDsInOrder" : productIDsInOrder, "orders" : orders, }, context_instance=context)#

def staffDeleteItems(request):
	# Require staff member to be logged in
	try:
		activeUser = request.session['username']
		activeStaff = request.session['staff']
		if activeStaff == False:
			return login_user(request)
	except KeyError:
		return login_user(request)

	#going to need a list of products to choose from
	allProducts = Product.objects.order_by('product_id')
	allOrders = Order.objects.order_by('order_id')
	allUsers = User.objects.order_by('user_id')

	errorMessage = ''
	error = False

	one = True
	two = True
	three = True
	#get the items to change
	#product works, order works, user works
	try:
		int(request.GET.get('productIDtoChange'))
		productToChange = allProducts.get(product_id=int(request.GET.get('productIDtoChange'))) 
		productToChange.delete()
	except ValueError:
		productToChange = None
		errorMessage = errorMessage + 'No such product exists to deleted;\n'
		one = False
	except Product.DoesNotExist:
		errorMessage = errorMessage + 'No such product exists to deleted;\n'
		productToChange = None
		one = False
	try:
		int(request.GET.get('orderIDtoChange'))
		orderToChange = allOrders.get(order_id=int(request.GET.get('orderIDtoChange'))) 
		orderToChange.delete()
	except ValueError:
		errorMessage = errorMessage +  ' No such order exists to deleted; \n'
		orderToChange = None	
		two = False
	except Order.DoesNotExist:
		errorMessage = errorMessage +  ' No such order exists to deleted; \n'
		orderToChange = None	
		two = False
	try:
		int(request.GET.get('userIDtoChange'))
		userToChange = allUsers.get(user_id=int(request.GET.get('userIDtoChange')))
		userToChange.delete() 
	except ValueError:
		errorMessage = errorMessage +  ' No such user exists to deleted; \n'
		userToChange = None
		three = False
	except User.DoesNotExist:
		errorMessage = errorMessage +  ' No such user exists to deleted; \n'
		userToChange = None	
		three = False


	if not one and not two and not three:
		error = True
	else:
		errorMessage = ''
	if error:
		return render_to_response('staffUpdate.html', {"errorMessage" : errorMessage, "allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=RequestContext(request))





	context = RequestContext(request)
	return render_to_response('staffUpdatesSaved.html', {}, context_instance=context)

def staffCreateItemsToAdd(request):
	# Require staff member to be logged in
	try:
		activeUser = request.session['username']
		activeStaff = request.session['staff']
		if activeStaff == False:
			return login_user(request)
	except KeyError:
		return login_user(request)


	context = RequestContext(request)
	return render_to_response('staffCreateItemsToAdd.html', {}, context_instance=context)

def staffAddItems(request):
	# Require staff member to be logged in
	try:
		activeUser = request.session['username']
		activeStaff = request.session['staff']
		if activeStaff == False:
			return login_user(request)
	except KeyError:
		return login_user(request)
	
	#get the items to change
	#follows same format as saveUpdate, needs to be done after saveUpdate is completed
	#get the items to change
	
	#get the items to change

	#here in case we reload the page
	allProducts = Product.objects.order_by('product_id')
	allOrders = Order.objects.order_by('order_id')
	allUsers = User.objects.order_by('user_id')

	errorMessage = ""


	#all 3 have to be checked first for response error handling
	if request.GET.get('productToChangeID'):
		myID = str(request.GET.get('productToChangeID'))
		productToChange = Product()
		try:
			Product.objects.get(product_id=myID)
			errorMessage = errorMessage + "Product ID already exists"
		except Product.DoesNotExist:
			productToChange.product_id = myID

	else:
		productToChange = None
	if request.GET.get('userToChangeID'):
		myID2 = str(request.GET.get('userToChangeID'))
		userToChange = User()
		try:
			User.objects.get(user_id=myID2)
			errorMessage = errorMessage + "User ID already exists"
		except User.DoesNotExist:
			userToChange.user_id = myID2
	else:
		userToChange = None
	if request.GET.get('orderToChangeID'):
		orderToChange = Order()
		myID3 = str(request.GET.get('orderToChangeID'))
		try:
			Order.objects.get(order_id=myID3)
			errorMessage = errorMessage + "Order ID already exists"
		except Order.DoesNotExist:
			orderToChange.order_id = myID3
	else:
		orderToChange = None


	#updates and error handling
	if request.GET.get('productToChangeID'):
		#update Product Values
		try:
			productToChange.product_name = str(request.GET.get('productName'))
			if productToChange.product_name is '': #cant be null
				raise ValueError('')
		except ValueError:
			errorMessage = errorMessage + "Invalid Product Name" + ";" 

		try:
			productToChange.product_description = str(request.GET.get('productDescription'))
			if productToChange.product_description is '': #cant be null
				raise ValueError('')
		except ValueError:
			errorMessage = errorMessage + "Invalid Product productDescription" + "; " 

		try:
			productToChange.product_price = int(request.GET.get('productPrice'))
			if productToChange.product_price < 0: #cant be negative
				raise ValueError('')
		except ValueError:
			errorMessage = errorMessage + "Invalid Product Price" + "; " 

		try:
			productToChange.product_active = bool(request.GET.get('productActive'))
		except ValueError:
			errorMessage = errorMessage + "Invalid Product Active" + "; " 

		try:
			productToChange.product_stock_quantity = int(request.GET.get('productStockQuantity'))
			if productToChange.product_stock_quantity < 0: #cant be negative
				raise ValueError('')
		except ValueError:
			errorMessage = errorMessage + "Invalid Product Stock quantity" + "; " 

		## so it doesn't break
		try:
			productToChange.supplies = Supplier.objects.get(supplier_id=int(request.GET.get('productSupplies')))
		except ValueError:
			errorMessage = errorMessage + "Invalid Product Supplier ID" + "; " 
		except Supplier.DoesNotExist:
			errorMessage = errorMessage + "Invalid Product Supplier ID" + "; " 

		
		#if error exists
		if errorMessage is not "":
			return render_to_response('staffCreateItemsToAdd.html', {"errorMessage" : errorMessage, "productToChange" : productToChange, "userToChange" : userToChange, "orderToChange" : orderToChange,"allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=RequestContext(request))
		#call isn't working for some reason???
		productToChange.save()

	else:
		productToChange = None
	if request.GET.get('orderToChangeID'):

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
		#update user values
		try:
			userToChange.user_name = str(request.GET.get('UserName'))
			if userToChange.user_name is '': #cant be null
				raise ValueError('')
			if len(userToChange.user_name) < 8:
				raise ValueError('NO')
		except ValueError:
			errorMessage = errorMessage + "Invalid username;"
		try:
			userToChange.user_password = str(request.GET.get('UserPassword'))
			if userToChange.user_password is '': #cant be null
				raise ValueError('')
			if len(userToChange.user_password) < 8:
				raise ValueError('NO')
		except ValueError:
			errorMessage = errorMessage + "Invalid password;"
		try:
			userToChange.user_address = str(request.GET.get('UserAddress'))
			if userToChange.user_address is '':
				raise ValueError('')
		except ValueError:
			errorMessage = errorMessage + "Invalid Address"
		try:
			userToChange.user_is_staff = bool(request.GET.get('UserIsStaff'))
		except ValueError:
			errorMessage = errorMessage + 'Invalid Staff'

		if errorMessage is not "":
			return render_to_response('staffCreateItemsToAdd.html', {"errorMessage" : errorMessage, "productToChange" : productToChange, "userToChange" : userToChange, "orderToChange" : orderToChange,"allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=RequestContext(request))

		userToChange.save()
	else:
		userToChange = None

	
	if not userToChange and not productToChange and not orderToChange:
		errorMessage = 'Nothing to add input'
		return render_to_response('staffCreateItemsToAdd.html', {"errorMessage" : errorMessage, "productToChange" : productToChange, "userToChange" : userToChange, "orderToChange" : orderToChange,"allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=RequestContext(request))

	context = RequestContext(request)	
	return render_to_response('browse.html', {"allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=context)

def staffUpdate(request):
	# Require staff member to be logged in
	try:
		activeUser = request.session['username']
		activeStaff = request.session['staff']
		if activeStaff == False:
			return login_user(request)
	except KeyError:
		return login_user(request)

	#going to need a list of products to choose from
	allProducts = Product.objects.order_by('product_id')
	allOrders = Order.objects.order_by('order_id')
	allUsers = User.objects.order_by('user_id')

	errorMessage = None 

	context = RequestContext(request)
	return render_to_response('staffUpdate.html', {"errorMessage" : errorMessage, "allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=RequestContext(request))

def staffUpdateItems(request):
	# Require staff member to be logged in
	try:
		activeUser = request.session['username']
		activeStaff = request.session['staff']
		if activeStaff == False:
			return login_user(request)
	except KeyError:
		return login_user(request)

	#going to need a list of products to choose from
	allProducts = Product.objects.order_by('product_id')
	allOrders = Order.objects.order_by('order_id')
	allUsers = User.objects.order_by('user_id')
	errorMessage = ''
	error = False
	#get the items to change
	#product works, order works, user works
	try:
		int(request.GET.get('productIDtoChange'))
		productToChange = allProducts.get(product_id=int(request.GET.get('productIDtoChange'))) 
	except ValueError:
		productToChange = None
		errorMessage = errorMessage + 'No such product exists to changed;\n'
	except Product.DoesNotExist:
		errorMessage = errorMessage + 'No such product exists to changed;\n'
		productToChange = None

	try:
		int(request.GET.get('orderIDtoChange'))
		orderToChange = allOrders.get(order_id=int(request.GET.get('orderIDtoChange'))) 
	except ValueError:
		errorMessage = errorMessage +  ' No such order exists to changed; \n'
		orderToChange = None	
	except Order.DoesNotExist:
		errorMessage = errorMessage +  ' No such order exists to changed; \n'
		orderToChange = None	
	try:
		int(request.GET.get('userIDtoChange'))
		userToChange = allUsers.get(user_id=int(request.GET.get('userIDtoChange'))) 
	except ValueError:
		errorMessage = errorMessage +  ' No such user exists to changed; \n'
		userToChange = None
	except User.DoesNotExist:
		errorMessage = errorMessage +  ' No such user exists to changed; \n'
		userToChange = None	


	if not userToChange and not productToChange and not orderToChange:
		error = True
	else:
		errorMessage = ''
	if error:
		return render_to_response('staffUpdate.html', {"errorMessage" : errorMessage, "allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=RequestContext(request))



	context = RequestContext(request)
	return render_to_response('staffUpdateItems.html', {"errorMessage" : errorMessage, "productToChange" : productToChange, "userToChange" : userToChange, "orderToChange" : orderToChange,"allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=context)

def staffSaveUpdates(request):
	# Require staff member to be logged in
	try:
		activeUser = request.session['username']
		activeStaff = request.session['staff']
		if activeStaff == False:
			return login_user(request)
	except KeyError:
		return login_user(request)

	#if the user is not staff
	#if User(activeUser).user_is_staff is False:
	#	return render_to_response('notStaff.html', context_instance=RequestContext(request))
	
	#get the items to change

	#here in case we reload the page
	allProducts = Product.objects.order_by('product_id')
	allOrders = Order.objects.order_by('order_id')
	allUsers = User.objects.order_by('user_id')

	#all 3 have to be checked first for response error handling
	if request.GET.get('productToChangeID'):
		myID = str(request.GET.get('productToChangeID'))
		productToChange = Product.objects.get(product_id=myID)
	else:
		productToChange = None
	if request.GET.get('userToChangeID'):
		myID2 = str(request.GET.get('userToChangeID'))
		userToChange = User.objects.get(user_id=myID2)
	else:
		userToChange = None
	if request.GET.get('orderToChangeID'):
		myID3 = str(request.GET.get('orderToChangeID'))
		orderToChange = Order.objects.get(order_id=myID3)
	else:
		orderToChange = None

	errorMessage = ""

	#updates and error handling
	if request.GET.get('productToChangeID'):
		#update Product Values
		try:
			productToChange.product_name = str(request.GET.get('productName'))
			if productToChange.product_name is '': #cant be null
				raise ValueError('')
		except ValueError:
			errorMessage = errorMessage + "Invalid Product Name" + ";" 

		try:
			productToChange.product_description = str(request.GET.get('productDescription'))
			if productToChange.product_description is '': #cant be null
				raise ValueError('')
		except ValueError:
			errorMessage = errorMessage + "Invalid Product productDescription" + "; " 

		try:
			productToChange.product_price = int(request.GET.get('productPrice'))
			if productToChange.product_price < 0: #cant be negative
				raise ValueError('')
		except ValueError:
			errorMessage = errorMessage + "Invalid Product Price" + "; " 

		try:
			productToChange.product_active = bool(request.GET.get('productActive'))
		except ValueError:
			errorMessage = errorMessage + "Invalid Product Active" + "; " 

		try:
			productToChange.product_stock_quantity = int(request.GET.get('productStockQuantity'))
			if productToChange.product_stock_quantity < 0: #cant be negative
				raise ValueError('')
		except ValueError:
			errorMessage = errorMessage + "Invalid Product Stock quantity" + "; " 

		## so it doesn't break
		try:
			productToChange.supplies = Supplier.objects.get(supplier_id=int(request.GET.get('productSupplies')))
		except ValueError:
			errorMessage = errorMessage + "Invalid Product Supplier ID" + "; " 
		except Supplier.DoesNotExist:
			errorMessage = errorMessage + "Invalid Product Supplier ID" + "; " 

		
		#if error exists
		if errorMessage is not "":
			return render_to_response('staffUpdateItems.html', {"errorMessage" : errorMessage, "productToChange" : productToChange, "userToChange" : userToChange, "orderToChange" : orderToChange,"allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=RequestContext(request))
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
		try:
			userToChange.user_name = str(request.GET.get('UserName'))
			if userToChange.user_name is '': #cant be null
				raise ValueError('')
			if len(userToChange.user_name) < 8:
				raise ValueError('NO')
		except ValueError:
			errorMessage = errorMessage + "Invalid username;"
		try:
			userToChange.user_password = str(request.GET.get('UserPassword'))
			if userToChange.user_password is '': #cant be null
				raise ValueError('')
			if len(userToChange.user_password) < 8:
				raise ValueError('NO')
		except ValueError:
			errorMessage = errorMessage + "Invalid password;"
		try:
			userToChange.user_address = str(request.GET.get('UserAddress'))
			if userToChange.user_address is '':
				raise ValueError('')
		except ValueError:
			errorMessage = errorMessage + "Invalid Address"
		try:
			userToChange.user_is_staff = bool(request.GET.get('UserIsStaff'))
		except ValueError:
			errorMessage = errorMessage + 'Invalid Staff'

		if errorMessage is not "":
			return render_to_response('staffUpdateItems.html', {"errorMessage" : errorMessage, "productToChange" : productToChange, "userToChange" : userToChange, "orderToChange" : orderToChange,"allProducts" : allProducts, "allOrders" : allOrders, "allUsers" : allUsers}, context_instance=RequestContext(request))

		userToChange.save()

	else:
		userToChange = None



	context = RequestContext(request)
	return render_to_response('staffUpdatesSaved.html', {"productToChange" : productToChange, "userToChange" : userToChange, "orderToChange" : orderToChange}, context_instance=context)

def account(request,round = 0):
	#Require user login, if not redirect to login page
	try:
		activeUser = request.session['username']
		if request.session['staff'].exist() == False:
			return login_user(request)
	except KeyError:
		return login_user(request)

	template = loader.get_template('account.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def accountUpdate(request):
	#Require user login, if not redirect to login page
	try:
		activeUser = request.session['username']
		if request.session['staff'].exist() == False:
			return login_user(request)
	except KeyError:
		return login_user(request)
	
	#initialize local reference variables
	newPasswordCheck = newPassword = newAddress = newEmail = ""

	#Check for POST request, if valid get action value
	if request.method == 'POST':
		form = AccountUpdateForm(request.POST)
		
		if form.is_valid():
		
			#Adssign update attributes
			newPassword = request.POST.get('password')
			newPasswordCheck = request.POST.get('repassword')
			newAddress = request.POST.get('address')
			newEmail = request.POST.get('email')
			
			#Load user reference
			user = User.objects.get(user_name = activeUser)
			
			#If new email is assigned, checks for uniqueness, if not unique, report and cycle
			if User.objects.filter(user_email = newEmail).exists() and user.user_email != newEmail:
				state = "Email already exists"
				print("Log: email already exists")
				return render(request, 'accountUpdate.html',{'form':form,'state':state})
			
			#Checks password matching, if not, report and cycle
			if newPassword != newPasswordCheck:
				state = "Your entered password does not match. Please re-enter"
				return render(request, 'accountUpdate.html',{'form':form,'state':state})

			# Attempt to update database, check successful, if successful return to account page
			user.user_password = newPassword
			user.user_email = newEmail
			user.user_address = newAddress
			user.save()
			print("Log: new user successfully created")
			state = "Account successfully updated!"
			return render(request,'accountUpdate.html',{'form':form,'state':state})

	#Initialize account form on first cycle
	else:
		form = AccountUpdateForm()
	
	state = "Enter updated account information"
	return render(request, "accountUpdate.html",{"form":form,"state":state})

def accountDelete(request):
	#Require user login, if not redirect to login page
	try:
		activeUser = request.session['username']
		if request.session['staff'].exist() == False:
			return login_user(request)
	except KeyError:
		return login_user(request)

	#Initialize reference variable(s)
	confirm = ""

	#Check for POST request, if valid get action value
	if request.method == 'POST':
		form = AccountDeleteForm(request.POST)
		
		if form.is_valid():
			
			#Assign update attributes
			confirm = request.POST.get('confirm')
			
			#Load user reference
			user = User.objects.get(user_name = activeUser)
			
			#If confirmatin successfully given, delete account
			#Report and log success, cycle back to main account page
			if confirm == user.user_email:
				state = "Account successfully deleted"
				print("Log: " + user.user_name + " account deleted")
				
				#Delete user
				User.objects.filter(user_name = activeUser).delete()
				del request.session['username']
				return render(request, 'accountDelete.html',{'form':form,'state':state})
			
			#If confirmation unsuccessful, report and cycle page
			state = "Email confirmation incorrect"
			return render(request, 'accountDelete.html',{'form':form,'state':state})

	#Initialize account form on first cycle
	else:
		form = AccountDeleteForm()

	state = "Enter user email to confirm account deletion"
	return render(request, "accountDelete.html",{'form':form,'state':state})

def accountOrders(request):
	#Require user login, if not redirect to login page
	try:
		activeUser = request.session['username']
		if request.session['staff'].exist() == False:
			return login_user(request)
	except KeyError:
		return login_user(request)
	
	#orders = Order.objects.select_related('order_date','order_paid').get(orders = activeUser)
	
	orders = Order.objects.filter(orders__user_name = activeUser)
	return render(request,'accountOrders.html', {"orders" : orders})

@csrf_exempt
def login_user(request):
	#logout user from session
	try:
		del request.session['username']
		del request.session['staff']
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
					request.session['staff'] = user.user_is_staff
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

#on delete add to models.py
#testing adding, ordering, deleting, updating