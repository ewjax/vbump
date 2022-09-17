# vbump

Inspired by bumpversion, tbump, and others, this version bumping utility does similar things to the others but does not also automate the git workflow steps.

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
    - development or 'dev', example '3.4.5.119-dev.27'
    - production or 'prod', example '3.4.5.119'
  - The version information saved is very configurable.  Nothing is hard-coded, but examples are included with typical setups.
    - Typical semvar (major, minor, patch) fields
    - Development version fields, such as devtext and devnumber
    - Control of reset logic, i.e. when lower-level fields should 'reset' to 0 when the higher-level fields are bumped
    - Support for fields which do not reset, but continue to increment (a 'build number' field)
  
  - --current-version operation:
    - Reads version from [current_version] section of [.vbump.ini]
    - Returns string form, in either 'dev' or 'prod' versions
    - Syntax for 'dev' and 'prod' versions as indicated by [syntax] section of [.vbump.ini]
    - Example [syntax] section:
      - [syntax]
      - write_dev = {major}.{minor}.{patch}.{build}{devtext}{devnumber}
      - write_prod = {major}.{minor}.{patch}.{build}
  
  - Bump operation: 
    - reads version info from, and writes to, the [current_version] section of the .vbump.ini file
    - Fields are reset in the order listed in 'reset_order' fields in [bump] section of [.vbump.ini]
    - If no field is specified, will automatically bump 'auto' fields listed in [bump] section of [.vbump.ini]
    - Example [bump] section:
      - [bump]
      - reset_order = major, minor, patch, devnumber
      - auto = build, devnumber
  
  - Write operation: 
    - reads version info from the [current_version] section of [.vbump.ini]
    - writes to the output files indicated in the [write] section of [.vbump.ini]
      - scans each line of each file for version strings, using the 'read_regex' regular expression from the [syntax] section of [.vbump.ini]
      - if a version string is found, replaces that version string, in either 'dev' or 'prod' formats, with the new version info

  - 

usage: vbump.exe [-h] [-c [{dev,prod}]] [-b [BUMP]] [-w [{dev,prod}]] [-d]
                 [-q] [-i]

