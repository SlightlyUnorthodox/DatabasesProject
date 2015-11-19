from django.contrib import admin
#from django.contrib.sites.models import Site

#admin.site.register(Site)
# Register your models here.

from .models import User
from .models import Order
from .models import Supplier
from .models import Contains
from .models import Product

admin.site.register(User)
admin.site.register(Order)
admin.site.register(Supplier)
admin.site.register(Contains)
admin.site.register(Product)
