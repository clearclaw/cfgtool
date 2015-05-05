#! /usr/bin/env python

from setuptools import setup, find_packages
import pyver

__version__, __version_info__ = pyver.get_version (pkg = "cfgtool",
                                                   public = True)

setup (
    name = "cfgtool",
    version = __version__,
    description = "Cfgtool configuration management",
    long_description = file ("README.rst").read (),
    classifiers = [],
    keywords = "",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "http://kanga.nu/~claw/",
    license = "Creative Commons Attribution-ShareAlike 3.0 Unported",
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
