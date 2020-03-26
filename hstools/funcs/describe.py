#!/usr/bin/env python3

import sys
import json
import yaml
import argparse
from itertools import groupby
from hstools import hydroshare, log

logger = log.logger


def get_tree(group, items, path):
    sep = lambda i: i.split('/', 1)
    head = [i for i in items if len(sep(i)) == 2]
    tail = [i for i in items if len(sep(i)) == 1]
    gv = groupby(sorted(head), lambda i: sep(i)[0])
    return group, dict([(i, path+i) for i in tail] + [get_tree(g, [sep(i)[1] for i in v], path+g+'/') for g, v in gv])


def tree_print(d, indent=0, prefix=''):
#    file_middle = '├──'
#    folder_last = '│   '
    folder = '└──'
    for key, value in d.items():
        print(' ' * indent + f'{prefix} {str(key)}')
        if isinstance(value, dict):
            next_prefix = folder
            tree_print(value, indent+1, next_prefix)


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
    parser.add_argument('-y', '--yaml', default=True, action='store_true',
                        help='output in yaml format')
    parser.add_argument('-j', '--json', default=False, action='store_true',
                        help='output in json format')
    parser.add_argument('-l', '--long', default=False, action='store_true',
                        help='long output format')
    parser.add_argument('-t', '--terms', nargs='+', type=str,
                        help='specific metadata terms to return, e.g. ' +
                        'authors, abstract, date_created, etc.', )
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
            meta_dict = {k: v for k, v in vars(meta).items()
                         if not k.startswith('_')}

            if args.terms:
                # filter based on specified data types
                meta_filtered = {}
                for term in args.terms:
                    if term in meta_dict.keys():
                        meta_filtered[term] = meta_dict[term]
                    else:
                        logger.error(f'  - Unknown metadata term {term}')
                meta_dict = meta_filtered

            # if not verbose, remove some of the metadata
            elif not args.long:
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
                class literal(str):
                    pass

                def literal_presenter(dumper, data):
                    return dumper.represent_scalar('tag:yaml.org,2002:str',
                                                   data, style='|')
                yaml.add_representer(literal, literal_presenter)
                v = meta_dict['abstract']
                meta_dict['abstract'] = literal(v)
                print(yaml.dump(meta_dict))

            if args.json:
                # query scientific metadata
                print(json.dumps(meta_dict,
                                 indent=4,
                                 sort_keys=True))

            # organize files for tree printing
            urls = []
            for file_info in hs.getResourceFiles(r):
                rpth = file_info['url'].split('contents/')[-1]
                urls.append(rpth)
            ftree = dict([get_tree('tree', urls, '')])['tree']
            tree_print(ftree)

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
