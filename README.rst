===============================
utils for django-rest-framework
===============================

.. image:: https://secure.travis-ci.org/z4r/gaiarestframework.png?branch=master
   :target: http://travis-ci.org/z4r/gaiarestframework

Based on `django-rest-framework`_.

* Filter on query string
* Tree Navigation
* Hostname context processor
* Definition of `url`
* Utils to test a Resource
* Absolute URLs in pagination
* And More...

.. _django-rest-framework: http://github.com/tomchristie/django-rest-framework

INSTALLED_APP
-------------
::

    'gaiarestframework',  # TEMPLATE ISSUE: gRF before django
    'djangorestframework',
    'django.contrib.admin',


TEMPLATE_CONTEXT_PROCESSORS
---------------------------
::

    'gaiarestframework.context_processors.hostname'


TITLE 'n' VERSION
-----------------
::

    GAIA_TITLE = 'GAIA'
    GAIA_VERSION = 'beta'
    GAIA_PAGINATOR_LIMIT = 20


