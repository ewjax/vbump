import re
import copy
import argparse

import config


#
#
def increment(value: str) -> str:
    """
    Perform increment operation on string representation of a value, such as what would be obtained from an ini file

    Args:
        value: value to be incremented, e.g. '3' becomes '4'

    Returns:
        string representation of incremented value

    """
    rv = None
    if value.isdecimal():
        rv = f'{int(value) + 1}'
    return rv


#
#
def bump(fieldname: str = None) -> dict:
    """
    Bump operation, to increase indicated fieldname by 1, and reset all lower fields (as indicated in reset_order) to 0
        - 'auto' fields are also incremented by 1

    Args:
        fieldname: fieldname to be incremented, or 'None' to only increment 'auto' fields

    Returns:
        updated dictionary of version fields and values

    """
    reset_order = config.config_data['bump']['reset_order']
    reset_list = reset_order.split(', ')

    current_version_dict = config.config_data['current_version']

    # make a manual copy, since although the config.config representation as a dictionary works,
    # you can't print and debug with it
    new_version_dict = {}
    for key in current_version_dict.keys():
        new_version_dict[key] = current_version_dict[key]

    # to help with the reset logic later, create a dictionary of (k:v) of (fieldnames:reset_order)
    # the logic being, if we are going to bump field at index N, then all fields at index >N will reset to 0
    reset_dict = {}
    i = 0
    for field in reset_list:
        reset_dict[field] = i
        i += 1

    # start by incrementing all fields in bump.auto list
    auto_list = config.config_data['bump']['auto'].split(', ')
    for field in auto_list:
        if field in new_version_dict:
            cur_value = new_version_dict[field]
            new_value = increment(cur_value)
            if new_value:
                new_version_dict[field] = new_value

    # then bumping the requested field
    # note that if the requested field has already been bumped in the auto_list, don't bump it again
    if fieldname in new_version_dict and fieldname not in auto_list:
        cur_value = new_version_dict[fieldname]
        new_value = increment(cur_value)
        if new_value:
            new_version_dict[fieldname] = new_value

            # if we successfully bumped the requested field, now reset all downstream fields, as defined in
            # the [bump][reset_order] value of the ini file
            if fieldname in reset_dict:
                for key in reset_dict.keys():
                    # use the reset_dict dictionary we created earlier to determine if each field should be reset
                    if reset_dict[key] > reset_dict[fieldname]:
                        new_version_dict[key] = '0'

    return new_version_dict


#
#
def version(write_pattern: str, version_dict: dict) -> str:
    """
    create version string, using the f-string pattern in write_pattern, and field values are from the version_dict

    TODO note that a target present in the write_pattern, but not in the list of fields in version_dict,
    will cause an exception which we don't catch, because there is no graceful recovery

    Args:
        write_pattern: f-string format for the created string
        version_dict: dictionary of {key:val} where keys = fieldnames, val = field value

    Returns:
        string containing current version, in write_pattern format

    """

    # use **kwargs formatting to translate fieldnames into the write_pattern
    rv = write_pattern.format(**version_dict)
    return rv


def main():

    # *********************************************************************************************************
    # parse the command line
    cli_parser = argparse.ArgumentParser()

    # bump commands
    cli_parser.add_argument('-b', '--bump',
                            help='bump the indicated field [default = auto field(s)]',
                            nargs='?', type=str, const='auto')

    # report current version
    cli_parser.add_argument('-v', '--version',
                            help='report current version string from .ini file to stdout [default format = dev]',
                            nargs='?', type=str, const='dev', choices=['dev', 'prod'])

    # write current version to output files
    cli_parser.add_argument('-w', '--write',
                            help='write current version string to output files [default format = dev]',
                            nargs='?', type=str, const='dev', choices=['dev', 'prod'])

    # dry run?
    cli_parser.add_argument('-d', '--dryrun',
                            help='flag: report what actions will be taken, but do not actually take them',
                            action='store_true')

    # quiet
    cli_parser.add_argument('-q', '--quiet',
                            help='flag: perform all actions with no screen reports',
                            action='store_true')

    args = cli_parser.parse_args()
    print(args)

    # *********************************************************************************************************

    # load the ini file
    config.load(args.quiet)

    # *********************************************************************************************************

    # process version command
    if args.version:

        # it is a bit amazing that this works.  Handy that format() is written to properly deal with **kwargs, which as it happens,
        # the dictionary representation of the config.config objects are in exactly the right format to support
        current_version_dict = config.config_data['current_version']
        write_dev = config.config_data['syntax']['write_dev']
        write_prod = config.config_data['syntax']['write_prod']

        if args.version == 'dev':
            if not args.quiet:
                print(f'Current version (dev format):   {version(write_dev, current_version_dict)}')
        elif args.version == 'prod':
            if not args.quiet:
                print(f'Current version (prod format):  {version(write_prod, current_version_dict)}')

    # process bump command
    if args.bump:

        current_version_dict = config.config_data['current_version']
        write_dev = config.config_data['syntax']['write_dev']

        # determine which fieldname to bump
        fieldname = None
        if args.bump in current_version_dict.keys():
            fieldname = args.bump
        else:
            if args.bump != 'auto' and not args.quiet:
                print(f"    ['{args.bump}'] unrecognized field name")
                print(f'    Valid field names: {list(current_version_dict.keys())}')

        # do the bump and report what new version will be
        new_version_dict = bump(fieldname)
        if not args.quiet:
            print(f'Current version (dev format):   {version(write_dev, current_version_dict)}')
            print(f'New version (dev format):       {version(write_dev, new_version_dict)}')

    # do a write?  or wait until user answers Y/N?
    # now what

if __name__ == '__main__':
    main()
