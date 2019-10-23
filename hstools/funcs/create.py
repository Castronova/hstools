#!/usr/bin/env python3

import os
import sys
import argparse
from hstools import hydroshare, log

logger = log.logger


def create_resource(hs, abstract, title,
                    keywords=[],
                    content_files=[]):

    return hs.createResource(abstract,
                             title,
                             keywords=keywords,
                             content_files=content_files)


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
    parser.add_argument('-a', '--abstract', required=True,
                        type=str, nargs='+',
                        help='resource description')
    parser.add_argument('-t', '--title', required=True,
                        type=str, nargs='+',
                        help='resource title')
    parser.add_argument('-k', '--keywords', type=str, nargs='+', default=[],
                        help='space separated list of keywords')
    parser.add_argument('-f', '--files', type=str, nargs='+', default=[],
                        help='space separated list of files')
    parser.add_argument('-v', default=True, action='store_true',
                        help='verbose output')
    parser.add_argument('-q', default=False, action='store_true',
                        help='suppress output')
    set_usage(parser)


def main(args):

    if args.v:
        log.set_verbose()
    if args.q:
        log.set_quiet()

    title = ' '.join(args.title)
    abstract = ' '.join(args.abstract)

    # make sure input files exist
    for f in args.files:
        if not os.path.exists(f):
            raise Exception(f'Could not find file: {f}')
            sys.exit(1)

    # connect to hydroshare
    hs = hydroshare.hydroshare()
    if hs is None:
        raise Exception(f'Connection to HydroShare failed')
        sys.exit(1)

    # get the hydroshare data
    resource_id = create_resource(hs,
                                  abstract,
                                  title,
                                  keywords=args.keywords,
                                  content_files=args.files)

    # return the path to the data
    logger.info(f'\nhttps://hydroshare.org/resource/{resource_id}')


def short_help():
    return 'Create a new HydroShare resource'


def long_help():
    return 'Create a new HydroShare resource'


if __name__ == '__main__':

    desc = """CLI for retrieving resources from the HydroShare
           platform.
           """
    parser = argparse.ArgumentParser(description=long_help())
    args = parser.parse_args()
    main(args)
