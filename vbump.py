import sys
import re
import argparse
import textwrap

import config
import util
import _version

# command line arguments stored here
args = argparse.Namespace()


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
    Bump operation, to
        - 'auto' fields are incremented by 1
        - increase indicated fieldname by 1, and reset all lower fields (as defined in reset_order) to 0

    Args:
        fieldname: fieldname to be incremented, or 'None' to only increment 'auto' fields

    Returns:
        updated dictionary of {key:val} where keys = fieldnames, val = field value

    """
    reset_order = config.config_data['bump']['reset_order']
    reset_list = reset_order.split(', ')

    # get current version info from config file
    current_version_dict = config.config_data['current_version']

    # make a copy for modification
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

    TODO note that a field present in the write_pattern, but not in the list of fields in version_dict,
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


#
#
def write():

    if not args.quiet:
        print(f'Updating output files, format [{args.write}]')

    # get the list of output filenames from the ini file
    write_files = config.config_data['write']['files']
    write_file_list = write_files.split(', ')

    # walk the list of files
    for filename in write_file_list:
        if not args.quiet:
            print(f'-----------------Processing file: [{filename}]--------------------')

        try:
            # read entire contents of file into a list
            with open(filename, 'r') as f:
                line_list = f.readlines()

            # walk the list of lines, looking for version strings
            lines_modified = 0
            for ndx, line in enumerate(line_list):

                # parse each line for the presence of a version string
                newline = parse(line)
                if newline and newline != line:
                    # replace the original line in the list with the new one
                    line_list.pop(ndx)
                    line_list.insert(ndx, newline)

                    # print summary
                    if not args.quiet:
                        print(f'Current version line: {line}', end='')
                        print(f'New version line    : {newline}', end='')

                    # increment the lines modified counter
                    lines_modified += 1

            # show how many lines were modified
            if not args.quiet:
                print(f'Lines modified: {lines_modified}')

            # if not dryrun, write out results
            # todo save prev files as .bak versions??
            if not args.dry_run:
                with open(filename, 'w') as f:
                    f.writelines(line_list)
                print(f'File saved: [{filename}]')

        except FileNotFoundError as fnf:
            if not args.quiet:
                print(fnf)


#
#
def parse(line: str) -> None or str:
    """
    Parse a given line of text for the presence of a version string, as defined by
    'read_regex' in the configuration ini file

    Args:
        line: line of text to be parsed

    Returns:
        None if no version string is found, or modified line with new version string
    """
    # set up the read pattern
    regex = config.config_data['syntax']['read_regex']
    pre_regex = '(?P<pre>.*)'
    post_regex = '(?P<post>.*)'
    full_regex = pre_regex + regex + post_regex

    # set up the write pattern
    if args.write == 'dev':
        key = 'write_dev'
    elif args.write == 'prod':
        key = 'write_prod'
    else:
        key = 'write_dev'

    write_pattern = config.config_data['syntax'][key]
    pre_pattern = '{pre}'
    post_pattern = '{post}'
    full_pattern = pre_pattern + write_pattern + post_pattern

    # default return value
    rv = None

    # check this line for presence of a version string
    m = re.match(full_regex, line)
    if m:
        pre_value = m.group('pre')
        post_value = m.group('post')

        # get current version dictionary, and add the pre and post values to it
        version_dict = config.config_data['current_version']
        version_dict['pre'] = pre_value
        version_dict['post'] = post_value

        # use the **kwargs format to smerge together the f-string write pattern with the dictionary of field values
        newline = full_pattern.format(**version_dict)

        # update the return value
        rv = newline + '\n'

    # return value
    return rv


#
#
def main():

    # *********************************************************************************************************
    # parse the command line
    def formatter(prog): return argparse.RawTextHelpFormatter(prog, max_help_position=52)
    cli_parser = argparse.ArgumentParser(
                                         # formatter_class=argparse.RawTextHelpFormatter,
                                         formatter_class=formatter,
                                         # formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent(f'''
                                            Command line tool to automate version bumping.
                                                - No command line options is equivalent to '--bump' and '--write'
                                                - Master version maintained in [{config.ini_filename}]
                                            '''))
    # report current version
    cli_parser.add_argument('-c', '--current-version',
                            help="Return current version string in 'dev' (default) or 'prod' format\n"
                                 f"Reads version info from [current_version] section of [{config.ini_filename}]\n"
                                 f"String formatted as indicated in [syntax] section of [{config.ini_filename}]\n",
                            nargs='?', type=str, const='dev', choices=['dev', 'prod'])

    # bump commands
    cli_parser.add_argument('-b', '--bump',
                            help=f"Bump the indicated field\n"
                                 f"Default = 'auto' fields in [bump] section of [{config.ini_filename}]\n"
                                 f"Reads from, and writes to [current_version] section of [{config.ini_filename}]",
                            nargs='?', type=str, const='auto')

    # write current version to output files
    cli_parser.add_argument('-w', '--write',
                            help=f"Writes version string in 'dev' (default) or 'prod' format into the output file(s)\n"
                                 f"Reads version info from [current_version] section of [{config.ini_filename}]\n"
                                 f"Writes to output files as specified in the [write] section of [{config.ini_filename}]",
                            nargs='?', type=str, const='dev', choices=['dev', 'prod'])

    # dry run?
    cli_parser.add_argument('-d', '--dry-run',
                            help='flag: Report what actions will be taken, but do not actually take them',
                            action='store_true')

    # quiet
    cli_parser.add_argument('-q', '--quiet',
                            help='flag: Perform all actions with no screen reports',
                            action='store_true')

    # init
    cli_parser.add_argument('-i', '--init',
                            help='flag: Print sample config files to screen (stdout)',
                            action='store_true')

    # version of vbump
    cli_parser.add_argument('-v', '--vbump-version',
                            help='flag: Print version of vbump and exit',
                            action='store_true')

    # parse the command line
    global args
    args = cli_parser.parse_args()
    # todo - add a verbose option and include this in output?  very useful for debugging
    # if not args.quiet:
    #     print(args)

    # *********************************************************************************************************

    # load the ini file
    configloaded = config.load()

    # *********************************************************************************************************

    # process init command and exit
    # do this before the check on configloaded, so even if the config file wasn't loaded, the user still
    # has the chance to issue the --init command to create the ini file
    if args.init:
        if not args.quiet:
            util.print_example_files()
        sys.exit(0)

    # process vbump version command
    if args.vbump_version:
        if not args.quiet:
            print(f'{_version.__VERSION__}')
            sys.exit(0)

    # was there a problem loading the ini file?  if so, bail out
    if not configloaded:
        sys.exit(0)

    # make a copy of the version info dictionary
    new_version_dict = {}
    current_version_dict = config.config_data['current_version']
    for key in current_version_dict.keys():
        new_version_dict[key] = current_version_dict[key]

    # no command given on command line? interpret this as --bump and --write
    bumpwrite = False
    if args.current_version is None and args.bump is None and args.write is None:
        bumpwrite = True

    # process version command
    if args.current_version:

        # it is a bit amazing that this works.  Handy that format() is written to properly deal with **kwargs, which as it happens,
        # the dictionary representation of the config.config objects are in exactly the right format to support
        write_dev = config.config_data['syntax']['write_dev']
        write_prod = config.config_data['syntax']['write_prod']

        if args.current_version == 'dev':
            if not args.quiet:
                print(f'Current version (dev format):   {version(write_dev, current_version_dict)}')
        elif args.current_version == 'prod':
            if not args.quiet:
                print(f'Current version (prod format):  {version(write_prod, current_version_dict)}')

    # process bump command
    if args.bump or bumpwrite:

        # current_version_dict = config.config_data['current_version']
        write_dev = config.config_data['syntax']['write_dev']

        # determine which fieldname to bump
        if args.bump and args.bump in current_version_dict.keys():
            fieldname = args.bump
        else:
            fieldname = None
            if args.bump and args.bump != 'auto' and not args.quiet:
                print(f"    ['{args.bump}'] unrecognized field name")
                print(f'    Valid field names: {list(current_version_dict.keys())}')

        # do the bump and report what new version will be
        new_version_dict = bump(fieldname)
        if not args.quiet:
            print(f'Current version (dev format): {version(write_dev, current_version_dict)}')
            print(f'New version     (dev format): {version(write_dev, new_version_dict)}')

        # if any fields have changed, then save them back to the current dictionary, and write it to disk
        if args.dry_run is False:
            modified = False
            for fieldname in current_version_dict.keys():
                new_val = new_version_dict[fieldname]
                current_val = current_version_dict[fieldname]
                if new_val != current_val:
                    config.config_data['current_version'][fieldname] = new_val
                    modified = True

            if modified:
                config.save()
                if not args.quiet:
                    print(f'Updated version info saved to ini file [{config.ini_filename}]')

    # process write command
    if args.write or bumpwrite:
        write()


if __name__ == '__main__':
    main()
