#!/usr/bin/env python3

import os
import unittest
from hstools import auth


class TestAuth(unittest.TestCase):
    bauthfile = os.path.abspath('./test/hs_auth_basic')
    oauthfile = os.path.abspath('./test/hs_auth_oauth')

    def test_oauth(self):

        # test that exception is raised when authfile isn't found
        with self.assertRaises(Exception):
            hs = auth.oauth2_authorization(authfile='/tmp/auth')
            hs.session.close()

        # test that it works with correct auth_location path
        hs = auth.oauth2_authorization(authfile=self.oauthfile)
        self.assertTrue(hs is not None)
        hs.session.close()

    def test_basic_auth(self):

        # test that exception is raised when authfile isn't found
        with self.assertRaises(Exception):
            hs = auth.basic_authorization(authfile='/tmp/auth')
            hs.session.close()

        # test that it works with correct auth_location path
        hs = auth.basic_authorization(authfile=self.bauthfile)
        self.assertTrue(hs is not None)
        hs.session.close()


if __name__ == '__main__':
    unittest.main()
