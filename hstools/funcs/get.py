#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
from hstools import hydroshare, log

logger = log.logger


def get_resource(hs, resid, force=False):

    # remove old data it force
    if force:
        opath = os.path.join(hs.save_dir, resid)
        if os.path.exists(opath):
            shutil.rmtree(opath)

    return hs.getResource(resid)


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


def add_arguments(parser):

    parser.description = long_help()
    parser.add_argument('resource_id',
                        help='unique identifier of the HydroShare resource '
                             'to download')
    parser.add_argument('-d', '--save-dir', default='.',
                        help='location to save resources downloaded from '
                             'HydroShare.org')
    parser.add_argument('-f', default=False, action='store_true',
                        help='force replace HydroShare resource if it '
                             'already exists')
    parser.add_argument('-v', default=True, action='store_true',
                        help='verbose output')
    parser.add_argument('-q', default=False, action='store_true',
                        help='supress output')

    set_usage(parser)


def short_help():
    return 'Retrieve resource content from HydroShare'


def long_help():
    return """Retrieve resource content from the HydroShare using a globally
            unique identifier. This identifier is provided as part of the
            HydroShare resource URL. These downloaded content is structured
            in bagit format, more information can be found at:
            https://www.archivematica.org/en/docs/archivematica-1.4/user-manual/transfer/bags/
            """


def main(args):

    if args.v:
        log.set_verbose()
    if args.q:
        log.set_quiet()

    # create output directory if it doesn't already exist
    try:
        if not os.path.exists(args.save_dir):
            os.makedirs(args.save_dir)
    except Exception as e:
        raise Exception(f'Could not create output directory: {e}')
        sys.exit(1)

    # connect to hydroshare
    hs = hydroshare.hydroshare(save_dir=args.save_dir)
    if hs is None:
        sys.exit(1)

    # get the hydroshare data
    get_resource(hs, args.resource_id, args.f)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=long_help())
    add_arguments(parser)

    args = parser.parse_args()
    main(args)

