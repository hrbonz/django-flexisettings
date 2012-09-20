# Django settings for fashionme_web project.
import sys
import os

# add project folder to path for generic loading
SETTINGSPATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

# detect environment, if no settings/env.py or settings.env.ENV empty
# keep defaults
RUN_ENV = None
exec(open(os.path.join(SETTINGSPATH, 'env.py')).read())

# environment declaration takes precendence, convenient to run some
# quick tests
if 'RUN_ENV' in os.environ:
    RUN_ENV = os.environ['RUN_ENV']

# import default security file
exec(open(os.path.join(SETTINGSPATH, 'security.py')).read())

# import environment security files in locals()
if RUN_ENV:
    try:
        exec(open(
            os.path.join(SETTINGSPATH, 'security_%s.py' % RUN_ENV)).read()
        )
    except IOError:
        print "No security module for %s environment" % RUN_ENV

# import standard settings.py file
try:
    exec(open(os.path.join(SETTINGSPATH, 'settings.py')).read())
except IOError:
    print "Copy your settings.py file in settings/"
    raise

# import running environment settings
if RUN_ENV:
    try:
        exec(open(
            os.path.join(SETTINGSPATH, 'settings_%s.py' % RUN_ENV)).read()
        )
    except IOError:
        print "No settings module for %s environment" % RUN_ENV
