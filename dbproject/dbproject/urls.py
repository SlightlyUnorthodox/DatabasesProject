from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	#Status
	# Complete/Stable pages
	url(r'^login/','webstore.views.login_user'),
	url(r'^register/','webstore.views.register_user'),
	url(r'^index/', 'webstore.views.index'),
    url(r'^admin/', include(admin.site.urls)),

    #Stable Pages (need front-end/design touch ups)
    url(r'^$', 'webstore.views.browse'),
	url(r'^browse/','webstore.views.browse'),
	url(r'^account/','webstore.views.account'),
	url(r'^search/','webstore.views.search'),	## WILL BE PHASED OUT
	url(r'^order/','webstore.views.order'),	
	url(r'^updateOrder/','webstore.views.updateOrder'),
	url(r'^staffUpdate/','webstore.views.staffUpdate'),
	url(r'^accountUpdate/','webstore.views.accountUpdate'),

	#Currently broken
	url(r'^placeOrder/','webstore.views.placeOrder'),
	
	url(r'^staffUpdateItems/','webstore.views.staffUpdateItems'),
	url(r'^staffSaveUpdates/','webstore.views.staffSaveUpdates'),
	url(r'^staffCreateItemsToAdd/','webstore.views.staffCreateItemsToAdd'),
	url(r'^staffAddItems/','webstore.views.staffAddItems'),
	url(r'^staffDeleteItems/','webstore.views.staffDeleteItems'),
	    
)
