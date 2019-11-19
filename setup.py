# -*- coding: utf-8 -*-
import os
import setuptools
from distutils.core import setup, Command
import flexisettings

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# run unittest2 tests with 'python setup.py test'
class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from tests.run import runtests
        runtests()


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
    cmdclass={ 'test': TestCommand },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
