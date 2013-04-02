# -*- coding: utf-8 -*-
import os
import sys

ENVIRONMENT_VARIABLE = "FLEXI_WRAPPED_MODULE"


class SettingsProxy(object):
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


# trick to replace the module by a class instance
# see http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
# after importing flexisettings.settings, the module will actually be an
# instance of SettingsProxy.
sys.modules[__name__] = SettingsProxy()
