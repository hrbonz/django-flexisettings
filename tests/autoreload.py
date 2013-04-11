import unittest2 as unittest
from tests.base import BaseTestCase
import os

class AutoreloadTestCase(BaseTestCase):

    def setUp(self):
        super(AutoreloadTestCase, self).setUp()
        os.environ.setdefault(self.envvar,
            "%s.settings" % self.test_project)

    def test_autoreload(self):
        """Test if settings modules are available through sys.modules"""
        import flexisettings.settings
        import sys
        self.assertIn(
            '.'.join(
                ['flexisettings.wrapped', self.test_project, 'settings_t']),
            sys.modules
        )

    def test_module_file(self):
        """Test settings modules __file__ value"""
        import flexisettings.settings
        import sys
        self.assertEqual(
            os.path.join(
                self.current_dir,
                self.test_folder,
                self.test_project,
                'settings_t.py'),
            sys.modules['.'.join(
                ['flexisettings.wrapped', self.test_project, 'settings_t'])].__file__
        )


if __name__ == '__main__':
    unittest.main()
