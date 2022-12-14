# vbump

Inspired by bumpversion, tbump, and others, this version bumping utility improves on those by 
	a) very configurable, but also very easy to use to automate the version bumping process
	b) handles both 'development' and 'production' version numbers
	c) supports the typical semvar system, i.e. major.minor.patch versioning
	d) supports the concept of fields which do not reset when others do, allowing for a 'build' field that continually increments
	e) doesn't tangle itself up with the git workflow steps

usage: vbump [-h] [-c [{dev,prod}]] [-b [BUMP]] [-w [{dev,prod}]] [-d] [-q] [-i] [-v]

Concepts:
  - The "master" version information is maintained the [current_version] section of [.vbump.ini]
  - Example [current_version] section:
    - [current_version]
    - major = 3
    - minor = 4
    - patch = 5
    - build = 119
    - devtext = -dev.
    - devnumber = 27
  
  - The string form of the version info can be represented in two formats
    - development or 'dev', examples '3.4.5.119-dev.27', '3.4.5-rc27', etc
    - production or 'prod', example '3.4.5.119', '3.4.5', etc
  - The version information saved is very configurable.  Nothing is hard-coded, but examples are included with typical setups.
    - Typical semvar (major, minor, patch) fields
    - Development version fields, such as devtext and devnumber
    - Control of reset logic, i.e. when lower-level fields should 'reset' to 0 when the higher-level fields are bumped
    - Support for fields which do not reset, but continue to increment (a 'build number' field)
  
  - Command line option: --current-version [{dev,prod}] (default: dev)
    - Reads version from [current_version] section of [.vbump.ini]
    - Returns string form, in either 'dev' or 'prod' versions (default: 'dev')
    - Syntax for 'dev' and 'prod' versions as indicated by [syntax] section of [.vbump.ini]
    - Example [syntax] section:
      - [syntax]
      - write_dev = {major}.{minor}.{patch}.{build}{devtext}{devnumber}
      - write_prod = {major}.{minor}.{patch}.{build}
  
  - Command line option: --bump [field] (default = as indicated in 'auto')
    - reads version info from, and writes to, the [current_version] section of the .vbump.ini file
    - Fields are reset in the order listed in 'reset_order' fields in [bump] section of [.vbump.ini]
    - If no field is specified, will automatically bump 'auto' fields listed in [bump] section of [.vbump.ini]
    - Example [bump] section:
      - [bump]
      - reset_order = major, minor, patch, devnumber
      - auto = build, devnumber
  
  - Command line option: --write [{dev,prod}] (default: dev)
    - reads version info from the [current_version] section of [.vbump.ini]
    - writes to the output files indicated in the [write] section of [.vbump.ini]
      - scans each line of each file for version strings, using the 'read_regex' regular expression from the [syntax] section of [.vbump.ini]
      - if a version string is found, replaces that version string, in either 'dev' or 'prod' formats, with the new version info
    - Example sections:
      - [syntax]
      - read_regex = (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\.(?P<build>\d+)((?P<devtext>[^0-9]+)(?P<devnumber>\d+))?
      - [write]
      - files = _version.py, other_files_here.txt

  - Command line option: --dry-run
    - If set, will report what actions will be taken, but will not actually take them

  - Command line option: --quiet
    - If set, will take all actions without sending reports to the screen

  - Command line option: --init
    - Useful to create initial versions if .vbump.ini and _version.py
    - Echoes the files to screen (stdout), the user should redirect and edit as needed
    - Includes content for sample .vbump.ini files, _version.py files
        
  - Command line option: --version
    - Print version of vbump to stdout and exit


