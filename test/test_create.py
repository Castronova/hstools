#!/usr/bin/env python3

import os
import shutil
import unittest
from hstools import hydroshare
from hstools.resource import ResourceMetadata


class TestCreate(unittest.TestCase):
    testfile = 'testfile.txt'
    authfile = os.path.abspath('test/hs_auth_basic')

    def setUp(self):

        # create a file for testing
        with open(self.testfile, 'w') as f:
            f.write('this is a test file')

    def tearDown(self):
        # remove the test file
        os.remove(self.testfile)

    def test_no_files(self):

        title = 'unit testing'
        abstract = 'this is a resource created by a unittest'
        keywords = ['test']
        # test that resource is created successfully without files
        hs = hydroshare.hydroshare(authfile=self.authfile)
        try:
            resid = hs.createResource(abstract,
                                      title,
                                      keywords,
                                      content_files=[])
            self.assertTrue(resid is not None)
        except Exception as e:
            print(e.status_msg)

        scimeta = hs.getResourceMetadata(resid)
        self.assertTrue(type(scimeta) == ResourceMetadata)
        hs.hs.deleteResource(resid)
        hs.close()

    def test_file_doesnt_exist(self):
        title = 'unit testing'
        abstract = 'this is a resource created by a unittest'
        keywords = ['test']

        # test that an exception is raised if an input file doesn't exist
        hs = hydroshare.hydroshare(authfile=self.authfile)
        with self.assertRaises(Exception):
            resid = hs.createResource(abstract,
                                      title,
                                      keywords,
                                      content_files=['wrong_name.txt'])
        hs.close()

    def test_one_file(self):

        title = 'unit testing'
        abstract = 'this is a resource created by a unittest'
        keywords = ['test']

        # test that resource is created successfully
        hs = hydroshare.hydroshare(authfile=self.authfile)
        resid = hs.createResource(abstract,
                                  title,
                                  keywords,
                                  content_files=[self.testfile])
        self.assertTrue(resid is not None)

        scimeta = hs.getResourceMetadata(resid)
        self.assertTrue(type(scimeta) == ResourceMetadata)
        hs.hs.deleteResource(resid)
        hs.close()


if __name__ == '__main__':
    unittest.main()
