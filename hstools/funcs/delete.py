#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
from hstools import hydroshare, log

logger = log.logger

def delete_resource(hs, resid):

    return hs.deleteResource(resid)


def add_arguments(parser):
    parser.add_argument('resource_id',
                        nargs='+',
                        type=str,
                        help='unique HydroShare resource identifier to be ' +
                             'deleted')
    parser.add_argument('-v', default=True, action='store_true',
                        help='verbose output')
    parser.add_argument('-q', default=False, action='store_true',
                        help='supress output')


def main(args):

    if args.v:
        log.set_verbose()
    if args.q:
        log.set_quiet()

    # connect to hydroshare
    hs = hydroshare.hydroshare()
    if hs is None:
        raise Exception(f'Connection to HydroShare failed')
        sys.exit(1)

    for resid in args.resource_id:
        try:
            delete_resource(hs, resid)
        except Exception as e:
            print(f'  {str(e)}')


if __name__ == '__main__':

    desc = """Delete an existing HydroShare resource
           """
    parser = argparse.ArgumentParser(description=desc)
    args = parser.parse_args()
    main(args)
