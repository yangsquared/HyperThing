from django.conf.urls.defaults import *
import views
from views import validate
import os
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^$', views.homepage),
	url(r'^validate',views.validate),
	#(r'^/validate/(?P<url>)/$', views.test)
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',      {'document_root': os.path.join(settings.SITE_ROOT,'./static')}),
)
