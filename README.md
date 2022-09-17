# vbump

Inspired by bumpversion, tbump, and others, this version bumping utility does similar things to the others but does not also automate the git workflow steps.

Concepts:
  - The "master" version information is maintained the [current_version] section of the .vbump.ini file
  - The string form of the version info can be represented in two formats
    - development or 'dev'
    - production or 'prod'
  - The version information saved is very configurable.  Nothing is hard-coded, but examples are included with typical setups.
    - Typical semvar (major, minor, patch) fields
    - Development version fields, such as devtext and devnumber
    - Control of reset logic, i.e. when lower-level fields should 'reset' to 0 when the higher-level fields are bumped
    - Support for fields which do not reset, but continue to increment (a 'build number' field)
  - Current Version operation:
    - Reads version from [current_version] section of [.vbump.ini]
    - Returns string form, in either 'dev' or 'prod' versions
    - Syntax for 'dev' and 'prod' versions as indicated by [syntax] section of [.vbump.ini]
      - Dev example: {major}.{minor}.{patch}.{build}{devtext}{devnumber}
      - Prod example: {major}.{minor}.{patch}.{build}
  - Bump operation: 
    - reads from, and writes to, the [current_version] section of the .vbump.ini file
    - Fields are reset in the order listed in 'reset_order' fields in [bump] section of [.vbump.ini]
    - If no field is specified, will automatically bump 'auto' fields listed in [bump] section of [.vbump.ini]
    - Example [bump] section:
      [bump]
      reset_order = major, minor, patch, devnumber
      auto = build, devnumber
  - Write operation: reads version info from the [current_version] section of the .vbump.ini file, and writes to 

usage: vbump.exe [-h] [-c [{dev,prod}]] [-b [BUMP]] [-w [{dev,prod}]] [-d]
                 [-q] [-i]

Command line tool to automate version bumping.
    - No command line options is equivalent to '--bump' and '--write'
    - Master version maintained in [.vbump.ini]

optional arguments:
  -h, --help                                       show this help message and exit
  -c [{dev,prod}], --current-version [{dev,prod}]  Return current version string in 'dev' (default) or 'prod' format
                                                   Reads version info from [current_version] section of [.vbump.ini]
                                                   String formatted as indicated in [syntax] section of [.vbump.ini]
  -b [BUMP], --bump [BUMP]                         Bump the indicated field
                                                   Default = 'auto' fields in [bump] section of [.vbump.ini]
                                                   Reads from, and writes to [current_version] section of [.vbump.ini]
  -w [{dev,prod}], --write [{dev,prod}]            Writes version string in 'dev' (default) or 'prod' format into the output file(s)
                                                   Reads version info from [current_version] section of [.vbump.ini]
                                                   Writes to output files as specified in the [write] section of [.vbump.ini]
  -d, --dry-run                                    flag: Report what actions will be taken, but do not actually take them
  -q, --quiet                                      flag: Perform all actions with no screen reports
  -i, --init                                       flag: Print sample config files to screen (stdout)
