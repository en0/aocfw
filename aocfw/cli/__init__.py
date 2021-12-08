from importlib import import_module
from os.path import dirname, basename, isfile, join
import glob


modules = glob.glob(join(dirname(__file__), "*.py"))

for f in modules:
    if not f.endswith("__init__.py") and not f.endswith("entry.py") and isfile(f):
        import_module("." + basename(f[:-3]), package="aocfw.cli")
