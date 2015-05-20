# -*- coding: utf-8 -*-
import os
import sys

from asyncio import get_event_loop, async, coroutine, sleep

_mtimes = {}
_win = (sys.platform == "win32")

_cached_modules = set()
_cached_filenames = []


def gen_filenames(only_new=False):
    """
    Returns a list of filenames referenced in sys.modules and translation
    files.
    """
    # N.B. ``list(...)`` is needed, because this runs in parallel with
    # application code which might be mutating ``sys.modules``, and this will
    # fail with RuntimeError: cannot mutate dictionary while iterating
    global _cached_modules, _cached_filenames
    module_values = set(sys.modules.values())
    _cached_filenames = clean_files(_cached_filenames)
    if _cached_modules == module_values:
        # No changes in module list, short-circuit the function
        if only_new:
            return []
        else:
            return _cached_filenames

    new_modules = module_values - _cached_modules
    new_filenames = clean_files(
        [filename.__file__ for filename in new_modules
         if hasattr(filename, '__file__')])

    _cached_modules = _cached_modules.union(new_modules)
    _cached_filenames += new_filenames
    if only_new:
        return new_filenames
    else:
        return _cached_filenames


def clean_files(filelist):
    filenames = []
    for filename in filelist:
        if not filename:
            continue
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        if filename.endswith("$py.class"):
            filename = filename[:-9] + ".py"
        if os.path.exists(filename):
            filenames.append(filename)
    return filenames


def code_changed():
    global _mtimes, _win
    for filename in gen_filenames():
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if _win:
            mtime -= stat.st_ctime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
            continue
        if mtime != _mtimes[filename]:
            _mtimes = {}
            return True
    return False


class Watcher(object):

    def __init__(self):
        self.running = False
        self.loop = get_event_loop()

    def _enqueue(self):
        if self.running:
            self.loop.call_soon_threadsafe(async, self.checkCode())

    def start(self):
        self.running = True
        self._enqueue()

    def stop(self):
        self.running = False

    @coroutine
    def checkCode(self):
        if code_changed():
            print("Change detected...\n")
            sys.exit(3)
        else:
            yield from sleep(1)
            self._enqueue()


def get_watcher():
    watcher = Watcher()
    watcher.start()
    return watcher