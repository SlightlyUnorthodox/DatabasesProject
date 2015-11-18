from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^$','home.views.index'),
    url(r'^webstore/', include('webstore.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
