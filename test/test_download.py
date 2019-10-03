#!/usr/bin/env python3

import os
import shutil
import unittest
from hstools import hydroshare


class TestDownload(unittest.TestCase):
    authfile = os.path.abspath('test/hs_auth_oauth')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_set_directory(self):
        """
        tests that the download directory is set properly
        """

        # test no download directory set
        hs = hydroshare.hydroshare(authfile=self.authfile)
        self.assertTrue(hs.download_dir == '.')
        hs.close()

        # test that an exception is raised if the save directory doesn't exist
        with self.assertRaises(Exception) as context:
            hs = hydroshare.hydroshare(authfile=self.authfile,
                                       save_dir='/dir_doesnt_exist')
        self.assertTrue('does not exist' in str(context.exception))
        hs.close()

        # test with directory as input
        d = 'test_directory_please_remove'
        os.makedirs(d)
        hs = hydroshare.hydroshare(authfile=self.authfile,
                                   save_dir=d)
        self.assertTrue(hs.download_dir == d)
        hs.close()
        os.rmdir(d)

    def test_get_file(self):

        # create a temp dir
        d = os.path.join(os.path.dirname(__file__),
                         'test_directory_please_remove')
        os.makedirs(d)

        # instantiate HS
        hs = hydroshare.hydroshare(authfile=self.authfile,
                                   save_dir=d)
        self.assertTrue(hs.download_dir == d)

        # download a published resource
        resid = '1be4d7902c87481d85b93daad99cf471'
        hs.getResource(resid)
        self.assertTrue(os.path.exists(os.path.join(d, f'{resid}')))

        # clean up
        hs.close()
        shutil.rmtree(d)


if __name__ == '__main__':
    unittest.main()
