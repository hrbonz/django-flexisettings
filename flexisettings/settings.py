# -*- coding: utf-8 -*-
import os
import sys

ENVIRONMENT_VARIABLE = "FLEXI_WRAPPED_MODULE"


class FlexiSettingsProxy(object):
    """Wrap configuration files following the app naming convention.

    For this app to work, the environment vairable
    'FLEXI_WRAPPED_MODULE' has to be set and point to django's settings.
    """

    _globals = {}
    _settings_path = None
    _wrapped_modules = []

    def __init__(self):
        try:
            settings_module = os.environ[ENVIRONMENT_VARIABLE]
            if not settings_module:
                raise KeyError
        except KeyError:
            raise ImportError("Flexisettings cannot be imported, " \
                "because environment variable %s is undefined." \
                % ENVIRONMENT_VARIABLE
            )
        self._settings_module = settings_module

        self._settings_path = self._get_mod_dir(settings_module)

        # import running environment
        self._import('env')
        # env variable supersedes file configuration
        if 'FLEXI_RUN_ENV' in os.environ:
            self._globals['FLEXI_RUN_ENV'] = os.environ['FLEXI_RUN_ENV']
        # import security file
        self._import('security')
        # import running env security file
        if 'FLEXI_RUN_ENV' in self._globals:
            self._import('security_%s' % self._globals['FLEXI_RUN_ENV'])
        # import main settings
        self._import('settings', False)
        # import running env settings
        if 'FLEXI_RUN_ENV' in self._globals:
            self._import('settings_%s' % self._globals['FLEXI_RUN_ENV'])

    # old-style class attribute lookup
    def __getattr__(self, name):
        return self.__getattribute__(name)

    # new-style class attribute lookup
    def __getattribute__(self, name):
        # break recursion when calling private attributes
        if name.startswith('_') and name != name.upper():
            return object.__getattribute__(self, name)
        if name in self._globals:
            return self._globals[name]

        return object.__getattribute__(self, name)

    def __dir__(self):
        return dir(object) + self._globals.keys()

    def _get_package(self, module):
        """return a package string extracted from a module import string.
        This should work because the settings module should be on the
        python import path, this is not using the django mechanism of
        :code:`app.module`.
        See https://docs.djangoproject.com/en/1.5/topics/settings/#envvar-DJANGO_SETTINGS_MODULE

        :param module: a module string as used in import command
        :type module: str
        """
        return '.'.join(module.split('.')[:-1])

    def _get_mod_dir(self, module):
        """return the module folder

        :param module: a module string as used in import command
        :type module: str
        """
        package = self._get_package(module)
        mod = __import__(package)
        modfile = mod.__file__
        #FIXME: this won't work on a non *NiX system
        if not modfile.startswith('/'):
            modfile = os.path.abspath(modfile)
        return os.path.dirname(modfile)

    def _import(self, modname, quiet=True):
        """import settings module and push configuration values to global scope

        :param modname: settings module name without package path, only
        the last part of a dotted name
        :type modname: str
        :param quiet: quietly fail if settings file does not exist
        :type quiet: bool
        """
        modfile = os.path.join(self._settings_path, modname) + '.py'
        globals_dict = dict(globals().items() + self._globals.items())
        # if the file doesn't exist but we want a quiet error
        if not os.path.isfile(modfile) and quiet:
            return

        execfile(modfile, globals_dict)
        # get which variables were set in modfile
        settings = set(globals_dict.keys()) - set(globals().keys())
        # push settings in _globals dict
        for setting in settings:
            if setting == setting.upper():
                self._globals[setting] = globals_dict[setting]
        # list this module as wrapped
        self._wrapped_modules.append(
            '.'.join([
                self._get_package(self._settings_module),
                modname
            ])
        )


# trick to replace the module by a class instance
# see http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
# after importing flexisettings.settings, the module will actually be an
# instance of SettingsProxy.
sys.modules[__name__] = FlexiSettingsProxy()
