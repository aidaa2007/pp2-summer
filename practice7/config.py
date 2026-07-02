from configparser import ConfigParser


def load_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    config = {}

    if parser.has_section(section):
        for k, v in parser.items(section):
            config[k] = v
    else:
        raise Exception("Section postgresql not found")

    return config