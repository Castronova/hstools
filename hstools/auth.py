#!/usr/bin/env python3

import os
import json
import base64
import pickle
import hs_restclient


def basic_authorization(authfile='~/.hs_auth_basic'):
    """
    performs basic HS authorization using username and password stored in
    ~/.hs_auth_basic file in the following format (b64 encoded):

    {
        "usr": "<username>"
        "pwd": "<password>"
    }

    Returns hs_restclient instance or None
    """

    authfile = os.path.expanduser(authfile)

    # exit if this file doesn't exist
    if not os.path.exists(authfile):
        raise Exception(f'Could not find authentication file '
                        f'[.hs_auth] at {authfile}')

    try:
        with open(authfile, 'r') as f:
            txt = f.read()
            d = base64.b64decode(txt)
            creds = json.loads(d.decode())
            a = hs_restclient.HydroShareAuthBasic(username=creds['usr'],
                                                  password=creds['pwd'])
            hs = hs_restclient.HydroShare(auth=a)
            hs.getUserInfo()
            return hs
    except Exception as e:
        raise Exception(e)

    # authorization failed
    return None


def oauth2_authorization(authfile='~/.hs_auth'):
    """
    performs HS authorization using OAuth2 credentials stored in
    ~/.hs_auth file, in a pickled binary format.

    Returns hs_restclient instance or None
    """

    authfile = os.path.expanduser(authfile)

    # exit if this file doesn't exist
    if not os.path.exists(authfile):
        raise Exception(f'Could not find authentication file '
                        f'[.hs_auth] at {authfile}')

    try:
        with open(authfile, 'rb') as f:
            token, cid = pickle.load(f)
            a = hs_restclient.HydroShareAuthOAuth2(cid, '', token=token)
            hs = hs_restclient.HydroShare(auth=a)
            hs.getUserInfo()
            return hs
    except Exception as e:
        raise Exception(e)

    # authorization failed
    return None
