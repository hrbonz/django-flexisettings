=========
Internals
=========


Layout
------

::

    myproject/__init__.py
              env.py
              security.py
              security_FLEXI_RUN_ENV.py
              settings.py
              settings_FLEXI_RUN_ENV.py

* ``env.py`` has a single variable ``FLEXI_RUN_ENV`` that defines a
  running environment. This variable is then used to call different
  profiles of configuration depending on the running environment like
  ``dev``, ``stage`` and ``prod``. The ``FLEXI_RUN_ENV`` variable can
  also be set by environment, the environment takes precedence over
  ``env.py``. Example::

        $ export FLEXI_RUN_ENV='dev'; python manage.py runserver

* ``security.py`` holds all the common security variables for the
  project, probably a good place for ``SECRET_KEY``.
* ``security_FLEXI_RUN_ENV`` specific environment security variables,
  dedicated database passwords should go there. Setting defined here
  will override settings defined in ``security.py``.
* ``settings.py`` the classic settings file found in all django projects.
* ``settings_FLEXI_RUN_ENV.py`` gathers local settings for a given
  running environment, settings defined here will override settings
  defined in ``settings.py``.


Loading order
-------------

The modules are loaded in the following order:

#. ``myproject/env.py``
#. ``myproject/security.py``
#. ``myproject/security_FLEXI_RUN_ENV.py``
#. ``myproject/settings.py``
#. ``myproject/settings_FLEXI_RUN_ENV.py``

If the ``FLEXI_RUN_ENV`` variable is false in python, the only settings
files read are ``security.py`` and ``settings.py``.
