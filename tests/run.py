import unittest2 as unittest

testmodules = (
    'tests.imports',
    'tests.settings',
    'tests.discovery',
    'tests.autoreload',
)

def runtests():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromNames(testmodules))
    unittest.TextTestRunner(verbosity=2).run(suite)
