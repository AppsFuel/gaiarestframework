from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^%s' % settings.ROOT_PATH, include('example.library.urls')),
    url(r'^restframework/', include('djangorestframework.urls', namespace='djangorestframework')),
)