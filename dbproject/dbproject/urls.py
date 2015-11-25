from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', include('webstore.urls')),
	url(r'^login/','webstore.views.login_user'),
	url(r'^register/','webstore.views.register_user'),
	url(r'^browse/','webstore.views.browse'),
	url(r'^account/','webstore.views.account'),
	#url(r'^$','home.views.index'),
    url(r'^index/', include('webstore.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
