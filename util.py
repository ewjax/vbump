

#
#
def print_example_files() -> None:
    """
    File to print sample files to stdout, suitable for capturing with command-line redirection and editing

    """
    print('')
    print('#------------------------------------------------------------------------------------------------------')
    print('# example .ini file, using fields: major, minor, patch, build, devtext, devnumber')
    print('')
    print('[current_version]')
    print('major = 0')
    print('minor = 0')
    print('patch = 0')
    print('build = 0')
    print('devtext = -dev.')
    print('devnumber = 0')
    print('')
    print('[syntax]')
    print('write_dev = {major}.{minor}.{patch}.{build}{devtext}{devnumber}')
    print('write_prod = {major}.{minor}.{patch}.{build}')
    print('read_regex = (?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)\\.(?P<build>\\d+)((?P<devtext>.+)(?P<devnumber>\\d+))?')
    print('')
    print('[bump]')
    print('reset_order = major, minor, patch, devnumber')
    print('auto = build, devnumber')
    print('')
    print('[write]')
    print('files = _version.py, other_files_here.txt')
    print('')
    print('#------------------------------------------------------------------------------------------------------')

    print('#------------------------------------------------------------------------------------------------------')
    print('# example _version.py file, using fields: major, minor, patch, build, devtext, devnumber')
    print('# version number')
    print("__VERSION__ = '0.0.0.0-dev.0'")
    print('')
    print('#------------------------------------------------------------------------------------------------------')

    print('#------------------------------------------------------------------------------------------------------')
    print('# example .ini file, using fields: major, minor, patch, devtext, devnumber')
    print('')
    print('[current_version]')
    print('major = 0')
    print('minor = 0')
    print('patch = 0')
    print('devtext = -dev.')
    print('devnumber = 0')
    print('')
    print('[syntax]')
    print('write_dev = {major}.{minor}.{patch}{devtext}{devnumber}')
    print('write_prod = {major}.{minor}.{patch}')
    print('read_regex = (?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)((?P<devtext>.+)(?P<devnumber>\\d+))?')
    print('')
    print('[bump]')
    print('reset_order = major, minor, patch, devnumber')
    print('auto = devnumber')
    print('')
    print('[write]')
    print('files = _version.py, other_files_here.txt')
    print('')
    print('#------------------------------------------------------------------------------------------------------')

    print('#------------------------------------------------------------------------------------------------------')
    print('# example _version.py file, using fields: major, minor, patch, devtext, devnumber')
    print('# version number')
    print("__VERSION__ = '0.0.0-dev.0'")
    print('')
    print('#------------------------------------------------------------------------------------------------------')

    # print('#------------------------------------------------------------------------------------------------------')
    # print('# !/bin/sh')
    # print('# this file is [<project root>/.git/hooks/precommit]')
    # print('./pre-commit.bat')
    # print('#------------------------------------------------------------------------------------------------------')
    #
    # print('rem ------------------------------------------------------------------------------------------------------')
    # print('rem this file is [<project root>/pre-commit.bat]')
    # print('vbump')
    # print('git add _version.py')
    # print('git add other_files_here.txt')
    # print('git add .vbump.ini')
    # print('rem ------------------------------------------------------------------------------------------------------')


# report width
REPORT_WIDTH = 100


# standalone function to print results to terminal window
def starprint(line: str, alignment: str = '<', fill: str = ' ') -> None:
    """
    utility function to print with leading and trailing ** indicators

    Args:
        line: line to be printed
        alignment: (left, centered, right) are denoted by one of (<, ^, >)
        fill: Character to fill with
    """
    width = REPORT_WIDTH
    print(f'** {line.rstrip():{fill}{alignment}{width}} **')
