#!/usr/bin/env python3

import sys
import json
import yaml
import argparse
from hstools import hydroshare, log

logger = log.logger


#def add_file(hs, resid, source, target):
#
#    return hs.addContentToExistingResource(resid, source, target=target)


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
                        nargs='+', type=str,
                        help='unique HydroShare resource identifier')
    parser.add_argument('-y', '--yaml', default=False, action='store_true',
                        help='output in yaml format')
    parser.add_argument('-j', '--json', default=False, action='store_true',
                        help='output in json format')
    parser.add_argument('-l', '--long', default=False, action='store_true',
                        help='long output format')
    parser.add_argument('-v', default=False, action='store_true',
                        help='verbose output')

    set_usage(parser)


def main(args):

    if args.v:
        log.set_verbose()

    # connect to hydroshare
    hs = hydroshare.hydroshare()
    if hs is None:
        raise Exception(f'Connection to HydroShare failed')
        sys.exit(1)

    if args.resource_id:
        print('-' * 50)

    # loop through input resources
    for r in args.resource_id:
        try:
            meta = hs.getResourceMetadata(r)
            meta_dict = {k: v for k, v in vars(meta).items() if not k.startswith('_')}

            # if not verbose, remove some of the metadata
            if not args.long:
                short_keys = ['abstract',
                              'authors',
                              'creators',
                              'date_created',
                              'title']
                meta_dict = {k: meta_dict[k] for k in short_keys}

                # clean strings
                for k, v in meta_dict.items():
                    if type(v) == type(str):
                        meta_dict[k] = v.replace('\n', '')

                # shorten author and creator data
                meta_dict['authors'] = ';'.join(meta_dict['authors'])

                creator_values = []
                for creator in meta_dict['creators']:
                    creator_values.append(creator['name'])
                meta_dict['creators'] = ';'.join(creator_values)


            if args.yaml:
                print(yaml.dump(meta_dict))

            if args.json:
                # query scientific metadata
                print(json.dumps(meta_dict,
                                 indent=4,
                                 sort_keys=True))
            print('-' * 50)

        except Exception as e:
            print(e)

def short_help():
    return 'Describe metadata and files'


def long_help():
    return """Describe the metadata and files of a HydroShare resource. By default a short summary is provided by the "-v" flag can be used for verbose output."""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=long_help())
    add_arguments(parser)

    args = parser.parse_args()
    main(args)
