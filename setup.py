#!/usr/bin/env python
# encoding: UTF-8

import ast
from setuptools import setup
import os.path

__doc__ = open(
    os.path.join(os.path.dirname(__file__), "README.rst"),
    "r"
).read()

try:
    # For setup.py install
    from carmen import __version__ as version
except ImportError:
    # For pip installations
    version = str(ast.literal_eval(
        open(os.path.join(
            os.path.dirname(__file__),
            "carmen",
            "__init__.py"),
            "r"
        ).read().split("=")[-1].strip()
    ))

setup(
    name="carmen",
    version=version,
    description="A dramatic screenplay",
    author="D Haynes",
    author_email="tundish@gigeconomy.org.uk",
    url="https://github.com/tundish/carmen_brittunculi",
    long_description=__doc__,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3"
        " or later (AGPLv3+)"
    ],
    packages=["carmen", "carmen.test"],
    package_data={
        "carmen": [
        ]
    },
    install_requires=[
        "turberfield-dialogue[audio]>=0.15.0",
        "turberfield-utils>=0.33.0",
    ],
    zip_safe=True,
    entry_points={}
)
