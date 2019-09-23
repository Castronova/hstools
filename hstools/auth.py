#!/usr/bin/env python3

import os
import json
import pickle
import hs_restclient


def basic_authorization():
    """
    performs basic HS authorization using username and password stored in
    ~/.hs_auth_basic file in the following format:

    {
        "usr": "<username>"
        "pwd": "<password>"
    }

    Returns hs_restclient instance or None
    """
    
    # get the authorization file for the default path
    authfile = os.path.expanduser("~/.hs_auth_basic")

    # exit if this file doesn't exist
    if not os.path.exists(authfile):
        return None

    try:
        with open(authfile, 'r') as f:
            creds = json.load(f)
            a = hs_restclient.HydroShareAuthBasic(username=creds['usr'],
                                                  password=creds['pwd'])
            hs = hs_restclient.HydroShare(auth=a)
            hs.getUserInfo()
            return hs
    except Exception as e:
        print(e)

    # authorization failed
    return None


def oauth2_authorization():
    """
    performs HS authorization using OAuth2 credentials stored in
    ~/.hs_auth file, in a pickled binary format.

    Returns hs_restclient instance or None
    """

    # get the authorization file for the default path
    authfile = os.path.expanduser("~/.hs_auth")

    # exit if this file doesn't exist
    if not os.path.exists(authfile):
        return None

    try:
        with open(authfile, 'rb') as f:
            token, cid = pickle.load(f)
            a = hs_restclient.HydroShareAuthOAuth2(cid, '', token=token)
            hs = hs_restclient.HydroShare(auth=a)
            hs.getUserInfo()
            return hs
    except Exception as e:
        print(e)

    # authorization failed
    return None
