========
Settings
========

Settings options
----------------

Settings options default values are set to ensure consistency with django
settings behavior. Most of the smartness, unicorns and rainbows are not enabled
by default.


DJANGO_SETTINGS_MODULE
^^^^^^^^^^^^^^^^^^^^^^

Environment variable to set to point at ``flexisettings.settings``, more
details in the `django documentation
<https://docs.djangoproject.com/en/dev/topics/settings/#envvar-DJANGO_SETTINGS_MODULE>`_.
This can be set by environment variable either on the command line, in
``manage.py`` or in ``myproject/wsgi.py``.


FLEXI_WRAPPED_MODULE
^^^^^^^^^^^^^^^^^^^^

Environment variable to set to point at your django settings, this environment
variable has to be set for ``flexisettings`` to work. This can be set by
environmentvariable either on the command line, in ``manage.py`` or in
``myproject/wsgi.py``.


FLEXI_RUN_ENV
^^^^^^^^^^^^^

Default: ``None``

String defining the running environment, used when trying to load settings
depending on the defined running environment.


FLEXI_SYS_PATH
^^^^^^^^^^^^^^

Default: ``['apps', 'lib']``

List of paths to add to ``sys.path`` if they exist, this will be done if
``FLEXI_LAYOUT_DISCOVERY`` is ``True``.


FLEXI_AUTORELOAD
^^^^^^^^^^^^^^^^

Default: ``True`` (this is django default behavior)

Boolean affecting the autoreload machinery for settings. If set to ``True``, it
should make the django autoreload code work when changing any settings file
found in ``flexisettings.settings._wrapped_modules``. If set to ``False``, the
autoreload will not work on settings. The code is a bit tricky, not guaranteed
to work and might have unsuspected effects, hence the possibility to disable.


FLEXI_LAYOUT_DISCOVERY
^^^^^^^^^^^^^^^^^^^^^^

Default: ``False``

Boolean that determines if ``flexisettings`` tries to be smart about your
project layout. It will add any ``FLEXI_MEDIA_FOLDER``,
``FLEXI_STATIC_FOLDER``, ``FLEXI_TEMPLATE_FOLDERS`` folder to the appropriate
configuration variables if they are not already set.


FLEXI_MEDIA_FOLDER
^^^^^^^^^^^^^^^^^^

Default: ``'media'``

The media folder name to look for when doing layout discovery.


FLEXI_STATIC_FOLDER
^^^^^^^^^^^^^^^^^^^

Default: ``'static'``

The static folder name to look for when doing layout discovery.


FLEXI_TEMPLATE_FOLDERS
^^^^^^^^^^^^^^^^^^^^^^

Default: ``('templates', )``

A tuple of templates folder names to look for when doing layout discovery.


FLEXI_SITE_ROOT
^^^^^^^^^^^^^^^

Default: ``FLEX_PROJECT_ROOT``

Path to the site root, everything that should not be tracked in a VCS but is
still part of your website. For example, the ``MEDIA_ROOT`` folder should
reside in the site root.


FLEXI_PROJECT_ROOT
^^^^^^^^^^^^^^^^^^

Default: ``dirname()`` of the settings folder

Path to the django project, basically everything that should be tracked in a
VCS.


Example configuration
---------------------

* edit ``env.py`` to set the working environment, let's use ``prod`` here::

        $ cat myproject/env.py
        # environment declaration
        FLEXI_RUN_ENV = 'prod'
* edit ``security.py`` to set the ``SECRET_KEY`` value::

        $ grep SECRET_KEY myproject/security.py
        SECRET_KEY = 'alongandcomplexsecretstring'
* set security variables in ``security_prod.py`` to be used in any settings
  file::

        $ grep DEFAULTDB myproject/security_prod.py
        DEFAULTDB_NAME = 'dbname'
        DEFAULTDB_USER = 'dbuser'
        DEFAULTDB_PWD = 'secret'
* edit ``settings_prod.py`` to override generic settings like ``DATABASES``,
  ``MEDIA_ROOT``, ``TIME_ZONE``::

        $ cat myproject/settings/settings_prod.py
        [...]
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': DEFAULTDB_NAME,
                'USER': DEFAULTDB_USER,
                'PASSWORD': DEFAULTDB_PWD,
                'HOST': '',
                'PORT': '',
            }
        }
        [...]
