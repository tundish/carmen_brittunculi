import ast
import os.path
import sys

from cx_Freeze import setup
from cx_Freeze import Executable

import turberfield

"""
To work, this script needs a version of cx_Freeze later than 2017-08-09:
https://github.com/anthony-tuininga/cx_Freeze

"""

try:
    from bluemonday_78 import __version__ as version
except ImportError:
    version = str(ast.literal_eval(
        open(os.path.join(os.path.dirname(__file__),
        "bluemonday78", "__init__.py"),
        'r').read().split("=")[-1].strip()
    ))

buildOptions = {
    "packages": [
        "asyncio.base_subprocess", "asyncio.constants", "asyncio.compat",
        "asyncio.selector_events",
        "pkg_resources._vendor.six", "pkg_resources._vendor.appdirs",
        "pkg_resources._vendor.packaging", "pkg_resources._vendor.pyparsing",
        "blessings", "tkinter", "turberfield.dialogue",
        "bluemonday78",
    ],
    "namespace_packages": ["turberfield"],
    "includes": [],
    "include_files": [],
    "excludes": []
}

if sys.platform == "win32":
    base = "Win32GUI"
    os.environ["TCL_LIBRARY"] = os.path.join(sys.base_exec_prefix, "tcl", "tcl8.6")
    os.environ["TK_LIBRARY"] = os.path.join(sys.base_exec_prefix, "tcl", "tk8.6")
    buildOptions["packages"].extend([
        "asyncio.proactor_events", "asyncio.windows_utils"
    ])
    buildOptions["include_files"].append(
        os.path.join(sys.base_exec_prefix, "DLLs", "tcl86t.dll")
    )
    buildOptions["include_files"].append(
        os.path.join(sys.base_exec_prefix, "DLLs", "tk86t.dll")
    )
elif sys.platform == "darwin":
    base = None
    buildOptions["packages"].append("_sysconfigdata_m_darwin_darwin")
else:
    base = None

if sys.version_info.major != 3:
    print("Supports Python 3 only.")
    sys.exit(1)

if sys.version_info.minor >= 6:
    buildOptions["packages"].extend([
        "asyncio.base_futures", "asyncio.base_tasks",
    ])

executables = [
    Executable(
        "bluemonday78/main.py",
        targetName="bluemonday.exe" if sys.platform == "win32" else "bluemonday",
        base=base
    )
]

setup(
    name="bluemonday78",
    version=version,
    description="A dramatic screenplay",
    options={
        "build_dmg": buildOptions,
        "build_exe": buildOptions,
    },
    executables=executables
)
