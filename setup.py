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
    packages=["carmen", "carmen.test", "carmen.utils"],
    package_data={
        "carmen": [
            "data/*.cfg",
            "dialogue/*/*.rst",
            "dialogue/*/*/*.rst",
            "static/audio/*.mp3",
            "static/css/*.css",
            "static/svg/*.svg",
            "templates/*.tpl",
        ]
    },
    install_requires=[
        "aiohttp>=2.3.10",
        "bottle>=0.12.13",
        "turberfield-dialogue>=0.18.0",
        "turberfield-utils>=0.34.0",
    ],
    extras_require={
        "dev": [
            "flake8>=3.5.0",
            "wheel>=0.30.0",
        ],
        "doc": [
            "cssselect>=1.0.3",
            "lxml>=4.2.3",
            "tinycss>=0.4",
            "pygal>=2.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "carmen-web = carmen.main:run",
        ],
    },
    zip_safe=True,
)
