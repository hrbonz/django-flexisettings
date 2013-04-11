import unittest2 as unittest
from tests.base import BaseTestCase
import os

class DiscoveryTestCase(BaseTestCase):

    def setUp(self):
        super(DiscoveryTestCase, self).setUp()
        os.environ.setdefault(self.envvar,
            "%s.settings" % self.test_project)

    def test_project_path(self):
        """Test project path"""
        import flexisettings.settings
        self.assertEqual(
            flexisettings.settings.FLEXI_PROJECT_ROOT,
            os.path.join(self.current_dir, self.test_folder)
        )

    def test_sys_path(self):
        """Test layout discovery"""
        import flexisettings.settings
        import sys
        self.assertIn(
            os.path.join(flexisettings.settings.FLEXI_PROJECT_ROOT, 'apps'),
            sys.path
        )

    def test_discovery_media(self):
        """Test media folder discovery"""
        import flexisettings.settings
        self.assertEqual(
            flexisettings.settings.MEDIA_ROOT,
            os.path.join(self.current_dir, self.test_folder, 'media')
        )

    def test_discovery_static(self):
        """Test static folder discovery"""
        import flexisettings.settings
        self.assertEqual(
            flexisettings.settings.STATIC_ROOT,
            os.path.join(self.current_dir, self.test_folder, 'static')
        )

    def test_discovery_templates(self):
        """Test templates folder discovery"""
        import flexisettings.settings
        self.assertIn(
            os.path.join(self.current_dir, self.test_folder, 'templates'),
            flexisettings.settings.TEMPLATE_DIRS,
        )

if __name__ == '__main__':
    unittest.main()
