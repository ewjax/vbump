import configparser

# global instance of the EQValet class
ini_filename = '.vbump.ini'


# global data
# begin by reading in the config data
config_data = configparser.ConfigParser()


def load() -> bool:
    """
    Utility function to load contents from .ini logfile into a configparser.ConfigParser object

    Returns:
        bool: Indicates success/failure loading the config file
    """
    global config_data

    rv = True
    file_list = config_data.read(ini_filename)
    try:
        if len(file_list) == 0:
            rv = False
            raise ValueError(f'Unable to open ini logfile [{ini_filename}]')
    except ValueError as verr:
        print(f'{str(verr)}, need to create it using the --init command line option')

    return rv


def save() -> None:
    """
    Utility function to save contents to .ini logfile from the configparser.ConfigParser object
    """
    global config_data
    with open(ini_filename, 'wt') as inifile:
        config_data.write(inifile)

    # # print out the contents
    # show()


def show() -> None:
    """
    print out the contents
    """
    global config_data

    print(f'{ini_filename} contents:')
    for section in config_data.sections():
        print(f'[{section}]')
        for key in config_data[section]:
            val = config_data[section][key]
            print(f'    {key} = {val}')
