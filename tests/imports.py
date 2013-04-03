import unittest
import sys
import os
import shutil

from django.core.management import call_command


class ImportTestCase(unittest.TestCase):

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

    def test_import_without_env(self):
        """Test importing flexisettings without setting environment
        variable FLEXI_WRAPPED_MODULE
        """
        try:
            import flexisettings.settings
        except ImportError, e:
            if "Flexisettings cannot be imported, because env" in str(e):
                pass
            else:
                raise
        except:
            raise
        else:
            self.fail(
                "No 'ImportError' exception when FLEXI_WRAPPED_MODULE not set"
            )

    def test_import(self):
        """Test importing flexisettings with environment variable set"""
        os.environ.setdefault(self.envvar,
            "%s.settings" % self.test_project)
        try:
            import flexisettings.settings
        except:
            self.fail(sys.exc_info()[1])

    def tearDown(self):
        if self.envvar in os.environ:
            os.environ.pop(self.envvar)
        sys.path.pop(0)
        os.chdir('..')
        shutil.rmtree(self.test_folder)

def suite():
    # it is necessary to run those tests in that order to avoid
    # namespace pollution with imported module
    tests = ['test_import_without_env', 'test_import']
    return unittest.TestSuite(map(ImportTestCase, tests))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
