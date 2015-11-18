# Testing django database syntax for online store implementation -Dax

from django.db import models

class User(models.Model):
	user_id = models.AutoField(primary_key=TRUE)
	user_name = models.CharField(max_length=50)
	user_password = models.CharField(max_length=50)
	user_address = models.CharField(max_length=50)
	user_email = models.CharField(max_length=50)
	user_is_staff = models.BooleanField(default=False)
	# many-to-one relationship "orders"
	# i.e./ many orders to one customer
	pass

class Order(models.Model):
	order_id = models.AutoField(primary_key=TRUE)
	order_date = models.DateField()
	order_paid = models.IntegerField()
	# many-to-one relationship "orders"
	orders = models.ForeignKey(User)
	# many-to-many relationship "contains"
	pass

class Supplier(models.Model):
	supplier_id = models.AutoField(primary_key=TRUE)
	supplier_name = models.CharField(max_length=50)
	# many-to-one relationship "supplys"
	# i.e./ many products to one supplier
	pass

class Product(models.Model):
	product_id = models.AutoField(primary_key=TRUE)	
	product_name = models.CharField(max_length=50)
	product_description = models.CharField(max_length=200)
	product_price = models.IntegerField()
	product_active = models.BooleanField(default=False)
	product_stock_quantity = models.IntegerField()
	# many-to-one relationship "supplys"
	supplys = models.ForeignKey(Supplier)
	# many-to-many relationship "contains"
	order = models.ForeignKey(Order)
	contains = models.ForeignKey(Contains)

# Structure for many-to-many relationship "contains"
class Contains(models.Model):
	quantity = models.IntegerField()
	products = models.ManyToManyField(Order,through='Product')