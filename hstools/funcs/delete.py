#!/usr/bin/env python3

import sys
import argparse
from hstools import hydroshare, log

logger = log.logger


def delete_resource(hs, resid):

    return hs.deleteResource(resid)


def delete_file(hs, resid, filename):

    return hs.deleteResourceFile(resid, filename)


def add_arguments(parser):

    parser.description = long_help()
    parser.add_argument('resource_id',
                        type=str,
                        help='unique HydroShare resource identifier to be ' +
                             'deleted')
    parser.add_argument('-a', default=False, action='store_true',
                        help='delete entire resource and all files')
    parser.add_argument('-f', '--files', required=False,
                        type=str, nargs='+',
                        help='files to add to remove from resource. Files must be contain path relative to the resource root directory.'
                        )
    parser.add_argument('-v', default=True, action='store_true',
                        help='verbose output')
    parser.add_argument('-q', default=False, action='store_true',
                        help='suppress output')
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

    if args.v:
        log.set_verbose()
    if args.q:
        log.set_quiet()

    if not (args.files or args.a):
        print('Please indicate to either delete the entire resource (-a) or specific files (-f). See "hs delete --help" for more information.')
        sys.exit(0)

    # connect to hydroshare
    hs = hydroshare.hydroshare()
    if hs is None:
        raise Exception(f'Connection to HydroShare failed')
        sys.exit(1)

    if args.a:
        try:
            delete_resource(hs, args.resource_id)
        except Exception as e:
            print(f'    REASON: {str(e)}')

    if args.files:
        for hsfile in args.files:
            try:
                delete_file(hs, args.resource_id, hsfile)
            except Exception as e:
                print(f'    REASON: {str(e)}')


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
