====================
Django-flexisettings
====================

Django flexible settings with running environment support, separate security
files and project layout detection.

Features:
    * get security configuration (passwords, secret key, API keys, etc) out of
      the main settings file
    * support multiple environments in a flexible way
    * automatic discovery and configuration of common project layouts


Information:
    * v0.2.5 is the last version which supports python 2.7


Installation
------------

::

    $ pip install django-flexisettings

No need to declare flexisettings in ``INSTALLED_APPS``.


Quickstart
----------

Development
^^^^^^^^^^^

Edit ``manage.py``, modify the value of ``DJANGO_SETTINGS_MODULE`` to point at
``flexisettings.settings`` and add ``FLEXI_WRAPPED_MODULE`` to point at your
project's settings::

    [...]
    if __name__ == "__main__":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flexisettings.settings")
        os.environ.setdefault("FLEXI_WRAPPED_MODULE", "myproject.settings")
    [...]


.. _wsgi-app-conf:

WSGI application
^^^^^^^^^^^^^^^^

Edit ``myproject/wsgi.py``, modify the value of ``DJANGO_SETTINGS_MODULE``
to point at ``flexisettings.settings`` and add ``FLEXI_WRAPPED_MODULE`` to
point at your project's settings::

    [...]
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flexisettings.settings")
    os.environ.setdefault("FLEXI_WRAPPED_MODULE", "myproject.settings")
    [...]


What now?
---------

This is all you need to get ``flexisettings`` to run your settings. At
this stage, **nothing** in the configuration object is changed, it is
simply wrapped in ``flexisettings`` proxy object.

`Read the docs <https://django-flexisettings.readthedocs.org/>`_ for more
powerful features of ``flexisettings``.


License
-------

django-flexisettings is published under a 3-clause BSD license, see the LICENSE
file included in the project.
