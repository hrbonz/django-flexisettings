# -*- coding: utf-8 -*-
import os
import sys

ENVIRONMENT_VARIABLE = "FLEXI_WRAPPED_MODULE"


class FlexiSettingsProxy(object):
    """Wrap configuration files following the app naming convention.

    For this app to work, the environment vairable
    'FLEXI_WRAPPED_MODULE' has to be set and point to django's settings.
    """

    _globals = {
        'FLEXI_SYS_PATH': ['apps', 'lib'],
        'FLEXI_AUTORELOAD': True,
        'FLEXI_LAYOUT_DISCOVERY': False,
        'FLEXI_MEDIA_FOLDER': 'media',
        'FLEXI_STATIC_FOLDER': 'static',
        'FLEXI_TEMPLATE_FOLDERS': ('templates', ),
    }
    _settings_path = None
    _wrapped_modules = {}

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

        self._import_settings()
        if self._globals['FLEXI_LAYOUT_DISCOVERY']:
            self._layout_discovery()
        if self._globals['FLEXI_AUTORELOAD']:
            for module, modfile in self._wrapped_modules.items():
                # add this module to sys.modules
                sys.modules['flexisettings.wrapped.%s' % module] = MockModule(module, modfile)

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
        return dir(object) + list(self._globals.keys())

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

    def _import_settings(self, quiet=True):
        """Get the settings imported in the proper order and depending
        on FLEXI_RUN_ENV variable.

        :param quiet: quietly fail if settings file does not exist
        :type quiet: bool
        """
        # import running environment
        self._import('env')
        # env variable supersedes file configuration
        if 'FLEXI_RUN_ENV' in os.environ:
            self._globals['FLEXI_RUN_ENV'] = os.environ['FLEXI_RUN_ENV']
        # import security file
        self._import('security', quiet)
        # import running env security file
        if 'FLEXI_RUN_ENV' in self._globals:
            self._import('security_%s' % self._globals['FLEXI_RUN_ENV'], quiet)
        # import main settings
        self._import('settings', False)
        # import running env settings
        if 'FLEXI_RUN_ENV' in self._globals:
            self._import('settings_%s' % self._globals['FLEXI_RUN_ENV'], quiet)

    def _import(self, modname, quiet=True):
        """import settings module and push configuration values to global scope

        The import order is as follow:
            * env.py
            * security.py
            * security_<FLEXI_RUN_ENV>.py, if FLEXI_RUN_ENV is set
            * settings.py, raises an IOError exception if missing
            * settings_<FLEXI_RUN_ENV>.py, if FLEXI_RUN_ENV is set

        :param modname: settings module name without package path, only
        the last part of a dotted name
        :type modname: str
        :param quiet: quietly fail if settings file does not exist
        :type quiet: bool
        """
        modfile = os.path.join(self._settings_path, modname) + '.py'
        globals_dict = {**globals(), **self._globals}
        # if the file doesn't exist but we want a quiet error
        if not os.path.isfile(modfile) and quiet:
            return

        exec(open(modfile).read(), globals_dict)
        # get which variables were set in modfile
        settings = set(globals_dict.keys()) - set(globals().keys())
        # push settings in _globals dict
        for setting in settings:
            if setting == setting.upper():
                self._globals[setting] = globals_dict[setting]
        # list this module as wrapped
        module = '.'.join([
            self._get_package(self._settings_module),
            modname
        ])
        self._wrapped_modules[module] = modfile

    def _site_dir(self, folder):
        """return an absolute path for a folder inside FLEXI_SITE_ROOT.

        :param folder: a folder name
        :type folder: str
        """
        return os.path.join(self._globals['FLEXI_SITE_ROOT'], folder)

    def _is_site_dir(self, folder):
        """returns a True if folder exists inside FLEXI_SITE_ROOT
        folder.

        :param folder: a folder name
        :type folder: str
        """
        return os.path.isdir(self._site_dir(folder))

    def _project_dir(self, folder):
        """return an absolute path for a folder inside
        FLEXI_PROJECT_ROOT.

        :param folder: a folder name
        :type folder: str
        """
        return os.path.join(self._globals['FLEXI_PROJECT_ROOT'], folder)

    def _is_project_dir(self, folder):
        """returns a True if folder exists inside FLEXI_PROJECT_ROOT
        folder.

        :param folder: a folder name
        :type folder: str
        """
        return os.path.isdir(self._project_dir(folder))

    def _layout_discovery(self):
        """perform layout detection:
            * set FLEXI_PROJECT_ROOT
            * set FLEXI_SITE_ROOT
            * add folders from FLEXI_SYS_PATH to sys.path
            * set MEDIA_ROOT
            * set STATIC_ROOT
            * add template folders to TEMPLATE_DIRS
        """
        # if project path is not specified, assume it's under the
        # settings folder
        if 'FLEXI_PROJECT_ROOT' not in self._globals:
            self._globals['FLEXI_PROJECT_ROOT'] = os.path.dirname(
                self._settings_path)
        self._project_path = self._globals['FLEXI_PROJECT_ROOT']
        # if site path is not specified, assume it is the same as
        # project path
        if 'FLEXI_SITE_ROOT' not in self._globals:
            self._globals['FLEXI_SITE_ROOT'] = self._project_path
        self._site_path = self._globals['FLEXI_SITE_ROOT']

        # add paths FLEXI_SYS_PATH to sys.path if they exist
        for folder in self._globals['FLEXI_SYS_PATH']:
            if self._is_project_dir(folder) \
                and self._project_dir(folder) not in sys.path:
                sys.path.insert(0, self._project_dir(folder))
            elif self._is_site_dir(folder) \
                and self._site_dir(folder) not in sys.path:
                sys.path.insert(0, self._site_dir(folder))

        # add media folder if MEDIA_ROOT is not already set or is empty
        if 'MEDIA_ROOT' not in self._globals \
            or not self._globals['MEDIA_ROOT']:
            folder = self._globals['FLEXI_MEDIA_FOLDER']
            if self._is_site_dir(folder):
                self._globals['MEDIA_ROOT'] = self._site_dir(folder)
            elif self._is_project_dir(folder):
                self._globals['MEDIA_ROOT'] = self._project_dir(folder)

        # add static folder if STATIC_ROOT is not already set or is empty
        if 'STATIC_ROOT' not in self._globals \
            or not self._globals['STATIC_ROOT']:
            folder = self._globals['FLEXI_STATIC_FOLDER']
            if self._is_site_dir(folder):
                self._globals['STATIC_ROOT'] = self._site_dir(folder)
            elif self._is_project_dir(folder):
                self._globals['STATIC_ROOT'] = self._project_dir(folder)

        # add templates folder if not in TEMPLATE_DIRS
        for folder in self._globals['FLEXI_TEMPLATE_FOLDERS']:
            if self._is_project_dir(folder) \
                not in self._globals['TEMPLATE_DIRS']:
                self._globals['TEMPLATE_DIRS'] += (
                    self._project_dir(folder),
                )


class MockModule(object):
    """An object mocking a module to use in sys.modules for django
    autoreload trickery.
    """
    def __init__(self, name, filename):
        self.__name__ = name
        self.__file__ = filename


# trick to replace the module by a class instance
# see http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
# after importing flexisettings.settings, the module will actually be an
# instance of SettingsProxy.
sys.modules[__name__] = FlexiSettingsProxy()
