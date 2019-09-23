#!/usr/bin/env python3

import os
import shutil
import unittest
from hstools import hydroshare


class TestDownload(unittest.TestCase):
    authfile = None
    authtemp = None
    backup_auth = None

    def setUp(self):
        # define the default authorization path
        self.authfile = os.path.expanduser("~/.hs_auth")
        self.authtemp = os.path.join(os.path.dirname(__file__),
                                     'hs_auth_oauth')

        # backup credentials if they already exist on the system
        backup_auth = None
        if os.path.exists(self.authfile):
            backup_auth = f'{self.authfile}.bak'
            shutil.move(self.authfile, backup_auth)

        # move credentials to default location
        shutil.copyfile(self.authtemp, self.authfile)

    def tearDown(self):

        # remove credentials from default location
        os.remove(self.authfile)

        # restore the original credentials if necessary
        if self.backup_auth is not None:
            shutil.move(self.backup_auth, self.authfile)

    def test_set_directory(self):
        """
        tests that the download directory is set properly
        """

        # test no download directory set
        hs = hydroshare.hydroshare()
        self.assertTrue(hs.download_dir == '.')
        hs.hs.session.close()

        # test that an exception is raised if the save directory doesn't exist
        with self.assertRaises(Exception) as context:
            hs = hydroshare.hydroshare(save_dir='/dir_doesnt_exist')
        self.assertTrue('does not exist' in str(context.exception))
        hs.hs.session.close()

        # test with directory as input
        d = 'test_directory_please_remove'
        os.makedirs(d)
        hs = hydroshare.hydroshare(save_dir=d)
        self.assertTrue(hs.download_dir == d)
        hs.hs.session.close()
        os.rmdir(d)

    def test_get_file(self):

        # create a temp dir
        d = os.path.join(os.path.dirname(__file__),
                         'test_directory_please_remove')
        os.makedirs(d)

        # instantiate HS
        hs = hydroshare.hydroshare(save_dir=d)
        self.assertTrue(hs.download_dir == d)

        # download a published resource
        resid = '1be4d7902c87481d85b93daad99cf471'
        hs.getResourceFromHydroShare(resid)
        self.assertTrue(os.path.exists(os.path.join(d, f'{resid}')))

        # clean up
        hs.hs.session.close()
        shutil.rmtree(d)







if __name__ == '__main__':
    unittest.main()
