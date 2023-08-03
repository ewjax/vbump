# vbump

Inspired by bumpversion, tbump, and others, this version bumping utility improves on those by 
	a) very configurable, but also very easy to use to automate the version bumping process
	b) handles both 'development' and 'production' version numbers
	c) supports the typical semvar system, i.e. major.minor.patch versioning
	d) supports the concept of fields which do not reset when others do, allowing for a 'build' field that continually increments
	e) doesn't tangle itself up with the git workflow steps

usage: vbump [-h] [-c [{dev,prod}]] [-b [BUMP]] [-w [{dev,prod}]] [-d] [-q] [-i] [-v]

### Concepts:
  - The "master" version information is maintained the [current_version] section of [.vbump.ini]
  - Example [current_version] section, defining the fieldnames (major, minor, patch, etc) and their current values:
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
    - Syntax for 'dev' and 'prod' versions as indicated by [syntax] section of [.vbump.ini], showing the arrangement of the fieldnames
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


### Build and Installation Steps:
The vbump utility makes use of a virtual python environment, and creates a standalone executable, which can be copied to a local directory such as /usr/local/bin or similar.

The build process is controlled via a makefile.

Build steps:
```
git clone git@github.com:ewjax/vbump.git
cd vbump
make venv
```
Activate the python virtual environment, then continue the build process:
```
(unix): source .vbump.venv/bin/activate
(windows): .vbump.venv\Scripts\activate
make all
Executable will be placed in ./dist subdirectory
```
Test the executable, by running it with the 'help' option:
```
./dist/vbump -h
```
Assuming it shows a list of command line options, indicating it built successfully, copy the vbump (or vbump.exe) executable from the /dist subdirectory to somewhere in your path.

Cleanup steps:
```
(while still in the python virtual environment): 
make clean
deactivate
make venv.clean
```