#!/usr/bin/env python3

import unittest
from hstools.hydroshare import hydroshare


class TestConnection(unittest.TestCase):

    def test_oauth(self):
        self.assertTrue(1)

    def test_basic_stored_file(self):
        """
        looks for credentials in ~/.hs_auth_basic
        """

        hs = hydroshare()


if __name__ == '__main__':
    unittest.main()
