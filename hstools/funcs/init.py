#!/usr/bin/env python3

import os
import sys
import json
import base64
import argparse
from getpass import getpass
from hstools import hydroshare


def init(loc='.'):

    fp = os.path.abspath(os.path.join(loc, '.hs_auth'))
    if os.path.exists(fp):
        print(f'Auth already exists: {fp}')
        remove = input('Do you want to replace it [Y/n]')
        if remove.lower() == 'n':
            sys.exit(0)
        os.remove(fp)

    usr = input('Enter HydroShare Username: ')
    pwd = getpass('Enter HydroShare Password: ')

    dat = {'usr': usr,
           'pwd': pwd}
    cred_json_string = str.encode(json.dumps(dat))
    cred_encoded = base64.b64encode(cred_json_string)
    with open(fp, 'w') as f:
        f.write(cred_encoded.decode('utf-8'))

    try:
        hydroshare.hydroshare(authfile=fp)
    except Exception:
        print('Authentication Failed')
        os.remove(fp)
        sys.exit(1)

    print(f'Auth saved to: {fp}')


def add_arguments(parser):

    parser.description = long_help()
    parser.add_argument('-d', '--dir', default='~',
                        help='location to save authentication directory ')
    set_usage(parser)


def set_usage(parser):

    optionals = []
    for option in parser._get_optional_actions():
        if len(option.option_strings) > 0:
            ostring = f'[{option.option_strings[0]}]'
            if '--' in ostring:
                # place '--' args at end of usage
                optionals.append(ostring)
            else:
                optionals.insert(0, ostring)

    positionals = []
    for pos in parser._get_positional_actions():
        positionals.append(pos.dest)
    parser.usage = f'%(prog)s {" ".join(positionals)} {" ".join(optionals)}'


def main(args):

    # create output directory if it doesn't already exist
    dir = os.path.expanduser(args.dir)
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except Exception as e:
        raise Exception(f'Could not save creds to directory {args.dir}: {e}')
        sys.exit(1)

    # initialize
    init(loc=dir)


def short_help():
    return 'Initialize a connection with HydroShare'


def long_help():
    return """Initialize a connection with HydroShare using basic
              username:password authentication. By default, credentials are
              stored in the $HOME directory in .hs_auth. All other hstools
              use this authentication to connect with HydroShare."""


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=long_help)
    add_arguments(parser)

    args = parser.parse_args()
    main(args)
