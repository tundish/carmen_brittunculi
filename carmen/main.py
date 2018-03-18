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
from collections import namedtuple
import logging
import random
import re
import sys

import bottle
import pkg_resources
from turberfield.utils.misc import log_setup

from carmen import __version__

DEFAULT_PAUSE = 1.2
DEFAULT_DWELL = 0.3

class World:

    Leaf = namedtuple("Leaf", ["ref", "x", "y"])

    contents = None

    regexp = re.compile("[0-9a-f]{32}")

    @staticmethod
    def forest(pitch=16):
        randint = random.randint
        return [
            World.Leaf("svg-leaf", x + randint(0, pitch), y + randint(0, pitch))
            for x in range(0, 480, pitch)
            for y in range(0, 480, pitch)
        ]

    def get_object(id):
        return World.contents.get(id)

    def object_id(obj):
        return getattr(obj, "id")

    def object_filter(config):
        print("Object filter with {0}".format(config))
        return World.regexp, World.get_object, World.object_id

def here():
    return bottle.template(
        pkg_resources.resource_string("carmen", "templates/forest.tpl").decode("utf8"),
        leaves=World.forest()
    )

def call(phrase):
    return {}

def move(location):
    return {}

def serve_css(filepath):
    log = logging.getLogger("carmen.main.serve_css")
    log.debug(filepath)
    locn = pkg_resources.resource_filename(
        "carmen", "static/css"
    )
    return bottle.static_file(filepath, root=locn)

def build_app():
    rv = bottle.Bottle()
    rv.router.add_filter("object", World.object_filter)
    rv.route("/", callback=here)
    rv.route("/call/<phrase:object>", callback=call)
    rv.route("/move/<location:object>", callback=move)
    rv.route("/css/<filepath:path>", callback=serve_css)

    return rv

def main(args):
    log = logging.getLogger(log_setup(args, "carmen"))

    bottle.debug(True)
    bottle.TEMPLATES.clear()
    log.debug(bottle.TEMPLATE_PATH)

    app = build_app()

    log.info("Starting server...")
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
