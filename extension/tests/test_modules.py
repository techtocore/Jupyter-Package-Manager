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
        self.assertIsNotNone(a)
    
    def test_create_project(self):
        a = pkg_manager.create_project('/SWAN_TEST', 'python3')
        flag = True
        try:
            if len(a['error']) > 0:
                flag = False
                print(a['error'])
        except:
            pass
        self.assertTrue(flag)

    # def test_search(self):
    #     a = pkg_manager.search('pyyaml')
    #     self.assertGreater()


if __name__ == '__main__':
    unittest.main()