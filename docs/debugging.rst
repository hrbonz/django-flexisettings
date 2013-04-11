=========
Debugging
=========

To help in the debugging process, it is possible to know which files
have been included in the final settings object by accessing
``flexisettings.settings._wrapped_modules``. An example from the unit
tests, the project name is 'testProject' and the running environment is
't'::

    $ python manage.py shell
    [...]
    >>> import flexisettings.settings
    >>> flexisettings.settings._wrapped_modules
    {'testProject.env': '/path/to/django-flexisettings/t/testProject/env.py',
     'testProject.security': '/path/to/django-flexisettings/t/testProject/security.py',
     'testProject.settings': '/path/to/django-flexisettings/t/testProject/settings.py',
     'testProject.settings_t': '/path/to/django-flexisettings/t/testProject/settings_t.py'}
