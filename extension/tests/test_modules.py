import unittest

import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../packagemanager'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from packagemanagement import PackageManager
pkg_manager = PackageManager()

class TestPackageManager(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        try:
            path = '/SWAN_TEST'
            os.mkdir(path)
            filepath = path + '/.swanproject'
            open(filepath, 'a').close()
        except:
            pass

    def test_list_projects(self):
        a = pkg_manager.list_projects()
        print(a)
        self.assertIsNotNone(a)


if __name__ == '__main__':
    unittest.main()