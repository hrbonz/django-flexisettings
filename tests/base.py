import unittest
import os
import shutil

from django.core.management import call_command


class SettingsTestCase(unittest.TestCase):

    test_folder = 't'
    test_project = 'testProject'

    def setUp(self):
        # create test folder
        os.mkdir(self.test_folder)
        # create a sample project
        call_command('startproject', self.test_project, self.test_folder)

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

    def tearDown(self):
        shutil.rmtree(self.test_folder)


if __name__ == "__main__":
    unittest.main()
