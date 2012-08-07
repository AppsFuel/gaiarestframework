===============================
utils for django-rest-framework
===============================

.. image:: https://secure.travis-ci.org/z4r/gaiarestframework.png?branch=master
   :target: http://travis-ci.org/z4r/gaiarestframework

Based on `django-rest-framework`_.

* Filter on query string
* Tree Navigation
* Hostname context processor
* Definition of Url
* Utils to test a Resource
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

