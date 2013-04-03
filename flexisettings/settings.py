# -*- coding: utf-8 -*-
import os
import sys

from django.utils import importlib

ENVIRONMENT_VARIABLE = "FLEXI_WRAPPED_MODULE"


class FlexiSettingsProxy(object):

    _globals = {
        # no running environment by default
        'FLEXI_RUN_ENV': None,
    }

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

        try:
            mod = importlib.import_module(self._settings_module)
        except ImportError, e:
            raise ImportError("Could not import settings '%s': %s" \
                % (self._settings_module, e)
            )
        self._mod = mod

    # old-style class attribute lookup
    def __getattr__(self, name):
        return self.__getattribute__(name)

    # new-style class attribute lookup
    def __getattribute__(self, name):
        # break recursion when calling private attributes
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        if name in self._globals:
            return self._globals[name]

        return object.__getattribute__(self, name)


# trick to replace the module by a class instance
# see http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
# after importing flexisettings.settings, the module will actually be an
# instance of SettingsProxy.
sys.modules[__name__] = FlexiSettingsProxy()
