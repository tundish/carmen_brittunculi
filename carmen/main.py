#!/usr/bin/env python
# encoding: UTF-8

# This file is part of Addison Arches.
#
# Addison Arches is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Addison Arches is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Addison Arches.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging
import re
import sys

import bottle
from turberfield.utils.misc import log_setup

from carmen import __version__

DEFAULT_PAUSE = 1.2
DEFAULT_DWELL = 0.3

class World:

    contents = None

    regexp = re.compile("[0-9a-f]{32}")

    def get_object(id):
        return World.contents.get(id)

    def object_id(obj):
        return getattr(obj, "id")

    def object_filter(config):
        print("Object filter with {0}".format(config))
        return World.regexp, World.get_object, World.object_id

def here():
    return "Hello World!"

def call(phrase):
    return "Hello World!"

def move(location):
    return "Hello World!"

def build_app():
    rv = bottle.Bottle()
    rv.router.add_filter("object", World.object_filter)
    rv.route("/", callback=here)
    rv.route("/call/<phrase:object>", callback=call)
    rv.route("/move/<location:object>", callback=move)

    return rv

def main(args):
    log = logging.getLogger(log_setup(args, "carmen"))
    log.info("Starting server.")

    app = build_app()
    bottle.run(app, host="localhost", port=8080, debug=True)

def parser(description=__doc__):
    rv = argparse.ArgumentParser(
        description,
        fromfile_prefix_chars="@"
    )
    rv.add_argument(
        "--version", action="store_true", default=False,
        help="Print the current version number")
    rv.add_argument(
        "-v", "--verbose", required=False,
        action="store_const", dest="log_level",
        const=logging.DEBUG, default=logging.INFO,
        help="Increase the verbosity of output")
    rv.add_argument(
        "--log", default=None, dest="log_path",
        help="Set a file path for log output")
    rv.add_argument(
        "--pause", type=float, default=DEFAULT_PAUSE,
        help="Time in seconds [{0:0.3}] to pause after a line.".format(DEFAULT_PAUSE)
    )
    rv.add_argument(
        "--dwell", type=float, default=DEFAULT_DWELL,
        help="Time in seconds [{0:0.3}] to dwell on each word.".format(DEFAULT_DWELL)
    )
    rv.add_argument(
        "--db", required=False, default=None,
        help="Database URL.")
    return rv


def run():
    p = parser()
    args = p.parse_args()

    rv = 0
    if args.version:
        sys.stdout.write(__version__)
        sys.stdout.write("\n")
    else:
        rv = main(args)

    if rv == 2:
        sys.stderr.write("\n Missing command.\n\n")
        p.print_help()

    sys.exit(rv)


if __name__ == "__main__":
    run()
