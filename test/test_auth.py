#!/usr/bin/env python3

import os
import shutil
import unittest
from hstools import auth


class TestAuth(unittest.TestCase):

    def test_oauth(self):
        """
        looks for credentials in ~/.hs_auth
        """

        # define the default authorization path
        authfile = os.path.expanduser("~/.hs_auth")
        authtemp = os.path.join(os.path.dirname(__file__), 'hs_auth_oauth')

        # backup credentials if they already exist on the system
        backup_auth = None
        if os.path.exists(authfile):
            backup_auth = f'{authfile}.bak'
            shutil.move(authfile, backup_auth)

        # move credentials to default location
        shutil.copyfile(authtemp, authfile)

        hs = auth.oauth2_authorization()
        self.assertTrue(hs is not None)

        # remove credentials from default location
        os.remove(authfile)

        # restore the original credentials if necessary
        if backup_auth is not None:
            shutil.move(backup_auth, authfile)

        hs.session.close()

    def test_basic_auth(self):
        """
        looks for credentials in ~/.hs_auth_basic
        """

        # define the default authorization path
        authfile = os.path.expanduser("~/.hs_auth_basic")
        authtemp = os.path.join(os.path.dirname(__file__), 'hs_auth_basic')

        # backup credentials if they already exist on the system
        backup_auth = None
        if os.path.exists(authfile):
            backup_auth = f'{authfile}.bak'
            shutil.move(authfile, backup_auth)

        # move credentials to default location
        shutil.copyfile(authtemp, authfile)

        hs = auth.basic_authorization()
        self.assertTrue(hs is not None)

        # remove credentials from default location
        os.remove(authfile)

        # restore the original credentials if necessary
        if backup_auth is not None:
            shutil.move(backup_auth, authfile)

        hs.session.close()


if __name__ == '__main__':
    unittest.main()
