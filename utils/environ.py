from os import environ


def env(key, default_value=None):
    val = environ.get(key, default_value) or default_value
    if default_value:
        return type(default_value)(val)
    return val