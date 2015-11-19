from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^login/','webstore.views.login_user'),
	url(r'^register/','webstore.views.register_user'),
	url(r'^$','home.views.index'),
    url(r'^index/', include('webstore.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
