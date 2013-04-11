import unittest2 as unittest
import sys
import os
import shutil

from django.core.management import call_command


class BaseTestCase(unittest.TestCase):

    test_folder = 't'
    test_project = 'testProject'
    envvar = 'FLEXI_WRAPPED_MODULE'

    secret_key = 'adummysecretkey'

    @classmethod
    def setUpClass(cls):
        # get current folder
        cls.current_dir = os.getcwd()
        if not os.path.isdir(cls.test_folder):
            # create test folder
            os.mkdir(cls.test_folder)
            # create a sample project
            call_command('startproject', cls.test_project, cls.test_folder)
            # create environment configuration
            env_fd = open(
                os.path.join(cls.test_folder, cls.test_project, 'env.py'),
                'w')
            env_fd.write("FLEXI_RUN_ENV = 't'\n")
            env_fd.close()
            # create security file
            sec_fd = open(
                os.path.join(cls.test_folder, cls.test_project, 'security.py'),
                'w')
            sec_fd.write("_SECRET_KEY = '%s'\n" % cls.secret_key)
            sec_fd.close()
            # create local settings file
            locset_fd = open(
                os.path.join(cls.test_folder, cls.test_project, 'settings_t.py'),
                'w')
            locset_fd.write("SECRET_KEY = _SECRET_KEY\n")
            locset_fd.write("FLEXI_LAYOUT_DISCOVERY = True\n")
            locset_fd.close()
            # add local apps, media, static, templates folders
            os.mkdir(os.path.join(cls.test_folder, 'apps'))
            os.mkdir(os.path.join(cls.test_folder, 'media'))
            os.mkdir(os.path.join(cls.test_folder, 'static'))
            os.mkdir(os.path.join(cls.test_folder, 'templates'))
            # add this location to sys.path for import
            sys.path.insert(0, os.path.join(os.getcwd(), cls.test_folder))

    def setUp(self):
        # change current directory to test folder
        os.chdir(self.test_folder)

    def tearDown(self):
        if self.envvar in os.environ:
            os.environ.pop(self.envvar)
        os.chdir('..')

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.current_dir)
        shutil.rmtree(cls.test_folder)
        # THIS IS AN UGLY HACK
        # if test_project is not removed, the next 'startproject'
        # command will fail. It is not possible at the present time to
        # really unload python modules.
        if cls.test_project in sys.modules:
            sys.modules.pop(cls.test_project)
