from django.conf.urls import patterns, include, url
from django.contrib import admin
from dbproject.home import views

urlpatterns = patterns('',
	url(r'^$','home.views.index'),
    url(r'^webstore/', include('webstore.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
