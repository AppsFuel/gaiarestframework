from django.conf.urls import patterns, url

from gaiarestframework.views import *

from .resources import *

urlpatterns = patterns(
    '',
    url(r'^author/$',
        GaiaListModelView.as_view(resource=AuthorResource),
        name='author_list'),
    url(r'^author/(?P<id>[^/]+)/$',
        GaiaReadModelView.as_view(resource=AuthorResource),
        name='author_info'),

    url(r'^author/(?P<author>[^/]+)/book/$',
        GaiaListOrCreateModelView.as_view(resource=BookResource),
        name='book_list'),
    url(r'^author/(?P<author>[^/]+)/book/(?P<id>[^/]+)/$',
        GaiaInstanceModelView.as_view(resource=BookResource),
        name='book_info'),

    url(r'^genre/$',
        AuthGaiaListOrCreateModelView.as_view(resource=GenreResource),
        name='genre_list'),
    url(r'^genre/(?P<description>[^/]+)/$',
        AuthGaiaInstanceModelView.as_view(resource=GenreResource),
        name='genre_info'),
)
