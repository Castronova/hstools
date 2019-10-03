#!/usr/bin/env python3

import os
import shutil
import unittest
from hstools import hydroshare
from hstools.resource import ResourceMetadata


class TestCreate(unittest.TestCase):
    testfile = 'testfile.txt'
    authfile = os.path.abspath('test/hs_auth_oauth')

    def setUp(self):

        # create a file for testing
        with open(self.testfile, 'w') as f:
            f.write('this is a test file')

    def tearDown(self):
        # remove the test file
        os.remove(self.testfile)

    def test_create_resource(self):

        title = 'unit testing'
        abstract = 'this is a resource created by a unittest'
        keywords = ['test']

        # test that resource is created successfully without files
        hs = hydroshare.hydroshare(authfile=self.authfile)
        resid = hs.createResource(abstract,
                                  title,
                                  keywords,
                                  content_files=[])
        self.assertTrue(resid is not None)

        scimeta = hs.getResourceMetadata(resid)
        self.assertTrue(type(scimeta) == ResourceMetadata)
        hs.hs.deleteResource(resid)
        hs.close()

        # test that an exception is raised if an input file doesn't exist
        hs = hydroshare.hydroshare(authfile=self.authfile)
        with self.assertRaises(Exception):
            resid = hs.createResource(abstract,
                                      title,
                                      keywords,
                                      content_files=['wrong_name.txt'])
        hs.close()

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


#    def test_get_file(self):
#
#        # create a temp dir
#        d = os.path.join(os.path.dirname(__file__),
#                         'test_directory_please_remove')
#        os.makedirs(d)
#
#        # instantiate HS
#        hs = hydroshare.hydroshare(save_dir=d)
#        self.assertTrue(hs.download_dir == d)
#
#        # download a published resource
#        resid = '1be4d7902c87481d85b93daad99cf471'
#        hs.getResource(resid)
#        self.assertTrue(os.path.exists(os.path.join(d, f'{resid}')))
#
#        # clean up
#        hs.hs.session.close()
#        shutil.rmtree(d)


if __name__ == '__main__':
    unittest.main()
