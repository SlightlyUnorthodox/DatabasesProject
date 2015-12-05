# Testing django database syntax for online store implementation -Dax


from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator


class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	def __unicode__(self):
		return self.user_id
	user_password = models.CharField(
		max_length=50,
		validators=[MinLengthValidator(8, "Your password must contain at least 8 characters.")],
		)
	def __unicode__(self):
		return self.user_password
	user_address = models.CharField(max_length=50)
	def __unicode__(self):
		return self.user_address
	user_email = models.CharField(max_length=50)
	def __unicode__(self):
		return self.user_email
	user_is_staff = models.BooleanField(default=False)
	#def __unicode__(self):
	#	return self.user_is_staff
	user_name = models.CharField(
		max_length=50, 
		validators=[MinLengthValidator(8, "Your username must contain at least 8 characters.")],
		unique=True)
	def __unicode__(self):
		return self.user_name
	# many-to-one relationship "orders"
	# i.e./ many orders to one customer
	pass

class Supplier(models.Model):
	supplier_id = models.AutoField(primary_key=True)
	def __unicode__(self):
			return self.supplier_id

	supplier_name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.supplier_name
	
	# many-to-one relationship "supplys"
	# i.e./ many products to one supplier
	pass



class Product(models.Model):
	product_id = models.AutoField(primary_key=True)	
	def __unicode__(self):
		return self.product_id
	product_description = models.CharField(max_length=1000)
	def __unicode__(self):
		return self.product_description
	product_price = models.IntegerField()
	def __unicode__(self):
		return self.product_price
	product_active = models.BooleanField(default=False)
	def __unicode__(self):
		return self.product_active
	product_stock_quantity = models.IntegerField()
	def __unicode__(self):
		return self.product_stock_quantity
	# many-to-many relationship "contains"
	#product does not need to reference order, or contains
	#orders = models.ForeignKey(Order)
	#def __unicode__(self):
	#	return '%s' % (self.orders)
	#contains = models.ForeignKey(Contains)
	#def __unicode__(self):
	#	return '%s' % (self.contains)
	product_name = models.CharField(max_length=50,default="Error: Bad product reference")
	def __unicode__(self):
		return self.product_name
	# many-to-one relationship "supplys"
	supplies = models.ForeignKey(Supplier)
	def __unicode__(self):
		return '%s' % (self.supplies)
	pass

# Structure for many-to-many relationship "contains"
class Contains(models.Model):
	quantity = models.IntegerField()
	def __unicode__(self):
		return self.quantity
	#one product can be in many Contains through its order (removed order bc reasons)
	productsLONGNAME = models.ManyToManyField(Product)
	def __unicode__(self):
		return '%s' % (self.productsLONGNAME)

class Order(models.Model):
	# many-to-many relationship "contains"
	contains = models.ForeignKey(Contains, null=True, blank=True)
	def __unicode__(self):
		return '%s' % (self.contains)



	order_id = models.AutoField(primary_key=True)
	def __unicode__(self):
		return self.order_id
	order_date = models.DateField()
	def __unicode__(self):
		return self.order_date
	order_paid = models.DecimalField(max_digits=19,decimal_places=2)
	def __unicode__(self):
		return self.order_paid
	# many-to-one relationship "orders"
	orders = models.ForeignKey(User)
	def __unicode__(self):
		return '%s' % (self.orders)
	
	pass
