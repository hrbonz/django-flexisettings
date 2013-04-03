import unittest
import sys
import os
import shutil

from django.core.management import call_command


class BaseTestCase(unittest.TestCase):

    test_folder = 't'
    test_project = 'testProject'
    envvar = 'FLEXI_WRAPPED_MODULE'

    def setUp(self):
        # create test folder
        os.mkdir(self.test_folder)
        # create a sample project
        call_command('startproject', self.test_project, self.test_folder)
        # change current directory to test folder
        os.chdir(self.test_folder)
        # add this location to sys.path for import
        sys.path.insert(0, os.getcwd())

    def tearDown(self):
        if self.envvar in os.environ:
            os.environ.pop(self.envvar)
        sys.path.pop(0)
        os.chdir('..')
        shutil.rmtree(self.test_folder)
