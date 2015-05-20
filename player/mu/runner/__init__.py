import os
import sys

# try:
#     from .notify import get_watcher
# except ImportError:
from .other import get_watcher


def restart_with_reloader():
    while True:
        args = [sys.executable]
        args += ['-W%s' % o for o in sys.warnoptions]
        args += sys.argv
        if sys.platform == "win32":
            args = ['"{0}"'.format(arg) for arg in args]
        new_environ = os.environ.copy()
        new_environ["RUN_MAIN"] = 'true'
        exit_code = os.spawnve(os.P_WAIT, sys.executable, args, new_environ)
        if exit_code != 3:
            return exit_code


def reloader(main_func):
    if os.environ.get("RUN_MAIN") == "true":
        notifier = get_watcher()
        main_func()
        notifier.stop()
    else:
        try:
            exit_code = restart_with_reloader()
            if exit_code < 0:
                os.kill(os.getpid(), -exit_code)
            else:
                sys.exit(exit_code)
        except KeyboardInterrupt:
            pass
