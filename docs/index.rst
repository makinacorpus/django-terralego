.. Django Terralego documentation master file, created by
   sphinx-quickstart on Fri Mar 17 12:19:48 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Terralego's documentation!
============================================

Getting started
---------------

Install using pip::

   pip install terralego

Add to your ``INSTALLED_APPS``::

   INSTALLED_APPS = [
      'django_terralego',
      ...
   ]

Set your credentials in your settings::

   TERRALEGO = {
       'USER': 'user',
       'PASSWORD': 'pass',
   }

You can also disable the request made to terralego if needed::

   TERRALEGO = {
       'ENABLED': False,
   }

Contents:

.. toctree::
   :maxdepth: 2

   geodirectory


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

