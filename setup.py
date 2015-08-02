#! /usr/bin/env python

try:
  import pyver # pylint: disable=W0611
except ImportError:
  import os, subprocess
  try:
    environment = os.environ.copy()
    cmd = "pip install pyver".split (" ")
    subprocess.check_call (cmd, env = environment)
  except subprocess.CalledProcessError:
    import sys
    print >> sys.stderr, "Problem installing 'pyver' dependency."
    print >> sys.stderr, "Please install pyver manually."
    sys.exit (1)
  import pyver # pylint: disable=W0611

from setuptools import setup, find_packages

__version__, __version_info__ = pyver.get_version (pkg = "cfgtool",
                                                   public = True)

setup (
    name = "cfgtool",
    version = __version__,
    description = "Cfgtool configuration management",
    long_description = file ("README.rst").read (),
    classifiers = [],
    keywords = "configuration management",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "https://pypi.python.org/pypi/cfgtool",
    license = "LGPL v3.0",
    packages = find_packages (exclude = ["tests",]),
    package_data = {
    },
    zip_safe = True,
    install_requires = [line.strip ()
                        for line in file ("requirements.txt").readlines ()],
    entry_points = {
        "console_scripts": [
            "cfgtool = cfgtool.main:main",
        ],
    },
)
