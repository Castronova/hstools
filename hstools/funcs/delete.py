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

    parser.description = long_help()
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


def short_help():
    return """Delete a HydroShare resource"""


def long_help():
    return """Delete HydroShare resource using a globally unique identifier.
              The identifier is provided as part of the HydroShare resource
              URL. WARNING: This action is permanent and cannot be undone.
           """


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=long_help())
    add_arguments(parser)

    args = parser.parse_args()
    main(args)
