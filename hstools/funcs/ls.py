#!/usr/bin/env python3

import sys
import json
import argparse
from enum import Enum
from hstools import hydroshare


class Filters(Enum):
    CREATOR = "creator"
    USER = "user"
    OWNER = "owner"
    AUTHOR = "author"
    GROUP = "group"
    TEXT = "full_text_search"
    PUBLISHED = "published"
    EDITABLE = "edit_permission"
    PUBLIC = "public"


def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def parse_filter(filter_str):

    try:
        f, v = filter_str.split('=')
        filter_keyword = getattr(Filters, f.upper()).value
        return {filter_keyword: v}
    except Exception:
        print(f'- invalid filter: {filter_str}')
        return None


def print_resource_list(hs, username, filter_dict={},
                        count=1000000, long_format=False,
                        size=False):

    # number of resource to query at a time
    qcount = 25

    kwargs = {'owner': username,
              'count': qcount}
    kwargs.update(filter_dict)
    cnt = 0
    for r in hs.hs.resources(**kwargs):

        cnt += 1
        if cnt > count:
            return

        res_line = f'{r["resource_id"]} '
        res_size_bytes = 0
        if size:
            try:
                files = json.loads(hs.hs.resource(r['resource_id']).files.all().content.decode())
                for f in files['results']:
                    res_size_bytes += int(f['size'])
            except Exception:
                res_size_bytes = -999

        if res_size_bytes > 0:
            res_line += f'[{humansize(res_size_bytes)}]'
        elif res_size_bytes < 0:
            res_line += f'[ERROR]'
        else:
            res_line += f'[?]'

        if not long_format:
            elip = '...' if len(r['resource_title']) > 25 else '   '
            print(f'+ {r["resource_title"][:25]:<25}{elip} - '
                  f'{res_line} ', flush=True)
        else:
            print(f'\n+ {res_line} ')
            print(f'   title: {r["resource_title"]}')
            print(f'   date created: {r["date_created"]}')
            print(f'   owner: {r["creator"]}')
            print(f'   authors: {", ".join(r["authors"])}')


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
    parser.add_argument('-l', default=False, action='store_true',
                        help='list in long format')
    parser.add_argument('-n', default=1000000, type=int,
                        help='number of resources to show')
    parser.add_argument('-s', default=False, action='store_true',
                        help='show resource size')
    parser.add_argument('-filter', nargs='*',
                        help='filter resource by metadata attribute, e.g '
                        'owner=<USERNAME> author=<USERNAME> '
                        'text=<FULL TEXT>. Multiple filters can be applied '
                        'at once by space separating them. Available filters '
                        'are: CREATOR, USER, OWNER, AUTHOR, GROUP, TEXT, '
                        'PUBLISHED, EDITABLE, PUBLIC')
    set_usage(parser)


def main(args):

    # check filter
    filters = {}
    if args.filter:
        for f in args.filter:
            pf = parse_filter(f)
            if pf is not None:
                filters.update(pf)
            else:
                sys.exit(1)

    # connect to hydroshare
    hs = hydroshare.hydroshare()
    userinfo = hs.userInfo()

    print_resource_list(hs, userinfo['username'], filter_dict=filters,
                        count=args.n, long_format=args.l, size=args.s)


def short_help():
    return 'List HydroShare resources that you own'


def long_help():
    return """List HydroShare resources that you own. Filters can be applied
              to limit which resources will be returned. For additional
              resource details, use the "-l" flag to print extra metadata. By
              default, all resources owned by the authenticated user will be
              returned, this can be limited using the "-n" flag.
           """


if __name__ == '__main__':

    desc = """List HydroShare resources
           """
    parser = argparse.ArgumentParser(description=desc)
    add_arguments(parser)

    args = parser.parse_args()
    main(args)
