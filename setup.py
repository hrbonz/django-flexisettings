# -*- coding: utf-8 -*-
import os
from distutils.core import setup
import flexisettings

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=flexisettings.__title__,
    version=flexisettings.__version__,
    author=u'LeDaPei',
    author_email='code@ledapei.com',
    packages=['flexisettings'],
    url=u'https://github.com/ledapei/django-flexisettings',
    license='3-clause BSD licence, see LICENCE.txt',
    description='Django flexible settings with running environment support, separate security files and project layout detection.',
    long_description=README,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: 3-clause BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
