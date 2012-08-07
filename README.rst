====================================
django-rest-framework utils for gaia
====================================

Mixins and Views for gaia.
Based on `django-rest-framework`_.

.. _django-rest-framework: http://github.com/tomchristie/django-rest-framework

INSTALLED_APP
-------------

::

    'gaiarestframework', #TEMPLATE ISSUE: gaia before django
    'djangorestframework',
    'django.contrib.admin',


TEMPLATE_CONTEXT_PROCESSORS
---------------------------

::

    'gaiarestframework.context_processor.hostname'
