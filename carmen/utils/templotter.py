#!/usr/bin/env python3
# encoding: UTF-8

# This file is part of Carmen Brittunculi.
#
# Carmen Brittunculi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Carmen Brittunculi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Carmen Brittunculi.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import itertools
import operator
import pathlib
import random
import sys

__doc__ = """
Create new files from a template and some names.

"""

DEFAULT_LOCATION = "."
DEFAULT_FORMAT = "{name}"
DEFAULT_SUFFIX = ".txt"

DEFAULT_NAMES = [
"about", "always", "approach", "ante", "attention", "action", "agency", "autonomy",
"zero", "zig", "zag", "zigzag", "zen", "zeal"
]

DEFAULT_TEMPLATE = """{name}
"""

def pick_one(names):
    names = sorted(names)
    print("", file=sys.stderr)
    print(
        *["{0}: {1}".format(n + 1, name) for n, name in enumerate(names)],
        sep="\n", file=sys.stderr
    )
    print("0: SKIP".format(len(names)), file=sys.stderr)
    print("=> ", end="", file=sys.stderr)
    choice = input()
    try:
        return None if not int(choice) else names[int(choice) - 1]
    except (IndexError, ValueError):
        return None

def generate_names(picker):
    for group, names in itertools.groupby(DEFAULT_NAMES, key=operator.itemgetter(0)):
        name = picker(list(names))
        if name is not None:
            yield name

def main(args):
    picker = pick_one if args.pick else random.choice
    names = args.names or generate_names(picker)
    template = args.template.read() if args.template else DEFAULT_TEMPLATE
    for n, name in enumerate(names):
        text = args.format.format(n, name=name)
        path = pathlib.Path(args.dir).expanduser().joinpath(text).with_suffix(args.suffix)
        path.touch()
        print(path.resolve(), file=sys.stdout)
        path.write_text(template.format(name=name, path=path.resolve()))
    return 0

def parser(description=__doc__):
    rv = argparse.ArgumentParser(
        description,
        fromfile_prefix_chars="@"
    )
    rv.add_argument(
        "--pick", default=False, action="store_true",
        help="interactively pick each name"
    )
    rv.add_argument(
        "--dir", default=DEFAULT_LOCATION, required=False,
        help="set a location for the new files [{0}]".format(DEFAULT_LOCATION)
    )
    rv.add_argument(
        "--format", default=DEFAULT_FORMAT, required=False,
        help="format string for each file name ['{0}']".format(DEFAULT_FORMAT)
    )
    rv.add_argument(
        "--suffix", default=DEFAULT_SUFFIX, required=False,
        help="add a suffix after each file name ['{0}']".format(DEFAULT_SUFFIX)
    )
    rv.add_argument(
        "--template", type=argparse.FileType("r"), required=False,
        help="define a template for new file content"
    )
    rv.add_argument("names", nargs="*", help="supply a list of file names")
    return rv
    

if __name__ == "__main__":
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)
