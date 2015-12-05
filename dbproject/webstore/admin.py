from django.contrib import admin
#from django.contrib.sites.models import Site

#admin.site.register(Site)
# Register your models here.

from .models import User
from .models import Order
from .models import Supplier
from .models import Contains
from .models import Product


class UserAdmin(admin.ModelAdmin):
	list_display = ['user_id','user_name','user_password','user_email','user_address','user_is_staff']
	list_editable = ['user_name','user_password','user_email','user_address','user_is_staff']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['order_id','order_date','order_paid','orders','contains']
	list_editable = ['order_date','order_paid','orders','contains']

class SupplierAdmin(admin.ModelAdmin):
	list_display = ['supplier_id','supplier_name']
	list_editable = ['supplier_name']

class ContainsAdmin(admin.ModelAdmin):
	list_display = ['quantity']
	list_editable = ['quantity']

class ProductAdmin(admin.ModelAdmin):
	list_display = ['product_id','product_description','product_price','product_active','product_stock_quantity','product_name','supplies']
	list_editable = ['product_description','product_price','product_active','product_stock_quantity','product_name','supplies']

admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Contains, ContainsAdmin)
admin.site.register(Product, ProductAdmin)
