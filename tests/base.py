import unittest2
import sys
import os
import shutil

from django.core.management import call_command


class BaseTestCase(unittest2.TestCase):

    test_folder = 't'
    test_project = 'testProject'
    envvar = 'FLEXI_WRAPPED_MODULE'

    @classmethod
    def setUpClass(cls):
        # create test folder
        os.mkdir(cls.test_folder)
        # create a sample project
        call_command('startproject', cls.test_project, cls.test_folder)
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
        shutil.rmtree(cls.test_folder)
