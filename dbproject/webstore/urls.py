from django.conf.urls import *
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = [
	url(r'^$',views.index, name ='index'),
]
