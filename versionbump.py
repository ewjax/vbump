import re
import copy


import config


def try_parse(ver):
    parse_dict = parse(ver)
    print(ver)
    print(parse_dict)


def parse(ver):

    current_version_dict = config.config_data['current_version']

    # make a manual copy, since although the config.config representation as a dictionary works,
    # you can't print and debug with it
    new_version_dict = {}
    for key in current_version_dict.keys():
        new_version_dict[key] = current_version_dict[key]

    regex = config.config_data['syntax']['read_regex']
    pre ='(?P<pre>.*)'
    post ='(?P<post>.*)'
    full_regex = pre + regex + post

    # get the list of fields from the keys present in the [current_version] section of the ini
    field_list = new_version_dict.keys()

    m = re.match(full_regex, ver)
    if m:
        pre = m.group('pre')
        new_version_dict['pre'] = pre

        for fieldname in field_list:

            # extract each value from the regex search
            # fieldnames present in [current_version] section of the ini, but not present in the regex,
            # will cause an exception to be thrown, which we will catch and ignore
            try:
                val = m.group(fieldname)
                new_version_dict[fieldname] = val
            except:
                pass

        post = m.group('post')
        new_version_dict['post'] = post

    # note that the returned dictionary will actually include two extra sections in it, 'pre' and 'post',
    # which include the contents of any line leading up to, and following, the version string
    return new_version_dict


def increment(value: str) -> str:
    rv = None
    if value.isdecimal():
        rv = f'{int(value) + 1}'
    return rv


def try_bump(token):
    print(f'bumping {token}')
    new_version_dict = bump(token)

    current_version_dict = config.config_data['current_version']

    for key in new_version_dict:
        print(f'{key}, current = {current_version_dict[key]}, new = {new_version_dict[key]}')


def bump(token):

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

    # start by bumping the requested field
    if token in new_version_dict:
        cur_value = new_version_dict[token]
        new_value = increment(cur_value)
        if new_value:
            new_version_dict[token] = new_value

            # if we successfully bumped the requested field, now reset all downstream fields, as defined in
            # the [bump][reset_order] value of the ini file
            if token in reset_dict:
                for key in reset_dict.keys():
                    # use the reset_dict dictionary we created earlier to determine if each field should be reset
                    if reset_dict[key] > reset_dict[token]:
                        new_version_dict[key] = '0'

    return new_version_dict






def version(write_pattern):

    # note that a target present in the write_pattern, but not in the list of fields in the [current_version] section of the ini,
    # will cause an exception which we don't catch, because there is no graceful recovery
    # todo - can we pre-scan the write pattern and identify all fields, and ensure we have a value for each?

    # it is a bit amazing that this works.  Handy that format() is written to properly deal with **kwargs, which as it happens,
    # the dictionary representation of the config.config objects are in exactly the right format to support
    rv = write_pattern.format(**config.config_data['current_version'])
    return rv


def main():

    config.load()


    ver = '3.4.5.99.rc.7'
    try_parse(ver)

    ver = '3.4.5.99.rc-7'
    try_parse(ver)

    ver = '3.4.5.99-dev.7'
    try_parse(ver)

    ver = '3.4.5.99_dev7'
    try_parse(ver)

    ver = '3.4.5.99@dev_7'
    try_parse(ver)

    ver = '3.4.5.99#dev-7'
    try_parse(ver)

    ver = '3.4.5.99 dev-7'
    try_parse(ver)

    ver = '3.4.5.99'
    try_parse(ver)


    ver = "version = '3.4.5.99.rc.7'"
    try_parse(ver)

    ver = "version = v3.4.5.99.rc.7"
    try_parse(ver)

    ver = 'version: 3.4.5.99.rc.7 and a bunch of other text'
    try_parse(ver)

    ver = 'version: 3.4.5.99 and a bunch of other text'
    try_parse(ver)

    ver = 'This document covers version 3.4.5.99 of the code'
    try_parse(ver)

    ver = "__VERSION__ = '3.4.5.99.rc.7'"
    try_parse(ver)


    x = '3'
    print(f'{x}, {increment(x)}')

    x = '45'
    print(f'{x}, {increment(x)}')

    x = 'xyzzy'
    print(f'{x}, {increment(x)}')

    print('************************************************************************')

    write_dev = config.config_data['syntax']['write_dev']
    write_prod = config.config_data['syntax']['write_prod']

    print(version(write_dev))
    print(version(write_prod))

    print('************************************************************************')

    try_bump('major')
    try_bump('minor')
    try_bump('patch')
    try_bump('build')
    try_bump('devtext')
    try_bump('devnumber')

if __name__ == '__main__':
    main()
