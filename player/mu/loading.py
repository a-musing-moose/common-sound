from importlib import import_module


def load_from_path(attrib_path):
    """
    Attempts to load a module attribute based on it's path
    """
    segments = attrib_path.split('.')
    if len(segments) < 2:
        raise ImportError("{0} is not a valid import path".format(attrib_path))
    attr = segments[-1]
    mod = import_module(".".join(segments[:-1]))
    return getattr(mod, attr)
