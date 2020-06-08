#!/usr/bin/env python3

import os
import unittest
from hstools import hydroshare


class TestAdd(unittest.TestCase):
    testfile = 'testfile1.txt'
    testfile2 = 'testfile2.txt'
    authfile = os.path.abspath('test/hs_auth_basic')
    title = 'unit testing'
    abstract = 'this is a resource created by a unittest'
    keywords = ['test']

    def setUp(self):

        # create a file for testing
        with open(self.testfile, 'w') as f:
            f.write('this is a test file')
        with open(self.testfile2, 'w') as f:
            f.write('this is a test file')

    def tearDown(self):
        # remove the test files
        os.remove(self.testfile)
        os.remove(self.testfile2)

    def test_add_file_to_resource(self):

        # test that resource is created successfully without files
        hs = hydroshare.hydroshare(authfile=self.authfile)
        resid = hs.createResource(self.abstract,
                                  self.title,
                                  self.keywords,
                                  content_files=[])
        self.assertTrue(resid is not None)

        resid = hs.addContentToExistingResource(resid, self.testfile)
        self.assertTrue(resid is not None)

        hs.hs.deleteResource(resid)
        hs.close()

    def test_add_wrong_path(self):

        hs = hydroshare.hydroshare(authfile=self.authfile)
        resid = hs.createResource(self.abstract,
                                  self.title,
                                  self.keywords,
                                  content_files=[])
        self.assertTrue(resid is not None)

        # test that an exception is raised if an input file doesn't exist
        with self.assertRaises(Exception):
            f = 'file_that_doesnt_exist.txt'
            resid = hs.addContentToExistingResource(resid, f)

        hs.hs.deleteResource(resid)
        hs.close()

    def test_add_multiple(self):

        hs = hydroshare.hydroshare(authfile=self.authfile)
        resid = hs.createResource(self.abstract,
                                  self.title,
                                  self.keywords,
                                  content_files=[])
        self.assertTrue(resid is not None)

        # test that resource is created successfully with list input
        files = [self.testfile, self.testfile2]
        for f in files:
            resid = hs.addContentToExistingResource(resid, f)
            self.assertTrue(resid is not None)

        # get file from resource, make sure it exists in the resource
        filenames = [r['file_name'] for r in hs.getResourceFiles(resid)]
        self.assertTrue(self.testfile in filenames)

        hs.hs.deleteResource(resid)
        hs.close()

    def test_file_already_exists(self):

        hs = hydroshare.hydroshare(authfile=self.authfile)
        resid = hs.createResource(self.abstract,
                                  self.title,
                                  self.keywords,
                                  content_files=[self.testfile])
        self.assertTrue(resid is not None)

        # test adding file that already exists in the resource
        with self.assertRaises(Exception):
            files = [self.testfile]
            resid = hs.addContentToExistingResource(resid, files)

        hs.hs.deleteResource(resid)
        hs.close()


if __name__ == '__main__':
    unittest.main()
