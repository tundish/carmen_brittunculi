#!/usr/bin/env python
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
from collections import namedtuple
import logging
import random
import re
import sys
import uuid

import bottle
import pkg_resources
from turberfield.dialogue.performer import Performer
from turberfield.utils.misc import log_setup

from carmen import __version__
import carmen.logic
from carmen.types import Coin
from carmen.types import Compass
from carmen.types import Location
from carmen.types import Marker
from carmen.types import Player
from carmen.types import Spot
from carmen.types import Via

DEFAULT_PAUSE = 1.2
DEFAULT_DWELL = 0.3

bottle.TEMPLATE_PATH.append(
    pkg_resources.resource_filename("carmen", "templates")
)

class World:

    Leaf = namedtuple("Leaf", ["ref", "x", "y"])
    quests = {}

    validation = {
        "email": re.compile(
            "[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]"
            "+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9]"
            "(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+"
            # http://www.w3.org/TR/html5/forms.html#valid-e-mail-address
        ),
        "location": re.compile("[0-9a-f]{32}"),
        "name": re.compile("[A-Z a-z]{2,32}"),
        "quest": re.compile("[0-9a-f]{32}"),
    }

    @staticmethod
    def forest(width, height, population=["svg-leaf-00", "svg-leaf-01"], pitch=(12, 9)):
        """
            TODO: Switch to better techniques, eg:

            http://devmag.org.za/2009/05/03/poisson-disk-sampling/
            https://codepen.io/alvov/pen/vgLevP (SVG lighting shader).
            https://css-tricks.com/look-svg-light-source-filters/

            Generate scenes in offline batches and select by eye.

        """
        choice = random.choice
        randint = random.randint
        pitch_x, pitch_y = pitch
        return [
            World.Leaf(choice(population), x + randint(0, pitch_x), y + randint(0, pitch_y))
            for x in range(0, width, pitch_x)
            for y in range(0, height, pitch_y)
        ]

    def get_object(id):
        return World.contents.get(id)

    def object_id(obj):
        return getattr(obj, "id")

    def object_filter(config):
        print("Object filter with {0}".format(config))
        return World.regexp, World.get_object, World.object_id

    @staticmethod
    def moves(quest_uid):
        try:
            asscns = World.quests[quest_uid]
        except KeyError:
            bottle.abort(401, "Quest {0!s} not found.".format(quest_uid))

        player = next(i for i in asscns.lookup if isinstance(i, Player))
        spot = player.get_state(Spot)

        locn = next(i for i in asscns.lookup if isinstance(i, Location) and i.get_state(Spot) == spot)
        neighbours = asscns.match(
            locn,
            forward=[Via.bidir, Via.forwd],
            reverse=[Via.bidir, Via.bckwd],
            predicate=lambda x: isinstance(x, Location)
        )
        moves = [
            (Compass.legend(i.get_state(Spot).value - spot.value), i)
            for i in neighbours
        ]
        return locn, moves

    @staticmethod
    def quest(name):
        uid = uuid.uuid4()
        asscns = carmen.logic.associations()
        start = next(iter(asscns.search(label="Green lane")))
        asscns.register(None, Player(name=name).set_state(start.get_state(Spot)))
        World.quests[uid] = asscns
        return uid

def get_start():
    return bottle.template(
        pkg_resources.resource_string("carmen", "templates/quest.tpl").decode("utf8"),
        validation=World.validation
    )

def post_start():
    log = logging.getLogger("carmen.main.start")
    name = bottle.request.forms.get("playername")
    email = bottle.request.forms.get("email")
    if not World.validation["name"].match(name):
        bottle.abort(401, "User input invalid name.")

    if not World.validation["email"].match(email):
        log.warning("User input invalid email.")
    else:
        log.info("Email offered: {0}".format(email))

    uid = World.quest(name)
    log.info("Player {0} created quest {1!s}".format(name, uid))
    bottle.redirect("/{0.hex}".format(uid))

def here(quest):
    log = logging.getLogger("carmen.main.here")
    uid = uuid.UUID(hex=quest)
    log.debug(uid)

    locn, moves = World.moves(uid)
    asscns = World.quests[uid]
    performer = Performer([carmen.logic.game], asscns.ensemble())
    if performer.stopped:
        log.warning("Game Over.")

    scene = performer.run(react=True)
    log.info(list(scene))

    width, height = 560, 400
    pitch = (12, 9)
    cell = (32, 32)
    # TODO: Do select. Use values.
    cast = {}
    coin = next((i for i in cast.values() if isinstance(i, Coin)), None)
    marker = next((i for i in cast.values() if isinstance(i, Marker)), None)
    return bottle.template(
        pkg_resources.resource_string("carmen", "templates/here.tpl").decode("utf8"),
        extent=(width + cell[0] - pitch[0], height + cell[1] - pitch[1]),
        leaves=World.forest(width, height, pitch=pitch),
        # leaves=[],
        here=locn,
        moves=moves,
        quest=uid,
        coin=coin,
        marker=marker
    )

def call(phrase):
    return {}

def move(quest, destination):
    log = logging.getLogger("carmen.main.move")
    quest_uid = uuid.UUID(hex=quest)
    log.debug(quest_uid)

    locn, moves = World.moves(quest_uid)

    dest_uid = uuid.UUID(hex=destination)
    log.debug(dest_uid)

    try:
        locn = next(i for i in dict(moves).values() if i.id == dest_uid)
        player = next(i for i in World.quests[quest_uid].lookup if isinstance(i, Player))
        player.set_state(locn.get_state(Spot))
        log.info("Player {0} moved to {1}".format(player, locn))
    except Exception as e:
        log.exception(e)
    finally:
        bottle.redirect("/{0.hex}".format(quest_uid))

def serve_css(filepath):
    log = logging.getLogger("carmen.main.serve_css")
    log.debug(filepath)
    locn = pkg_resources.resource_filename(
        "carmen", "static/css"
    )
    return bottle.static_file(filepath, root=locn)

def serve_svg(filepath):
    log = logging.getLogger("carmen.main.serve_svg")
    log.debug(filepath)
    locn = pkg_resources.resource_filename(
        "carmen", "static/svg"
    )
    return bottle.static_file(filepath, root=locn)

def build_app():
    rv = bottle.Bottle()
    rv.route("/", callback=get_start, method="GET")
    rv.route("/", callback=post_start, method="POST")
    rv.route("/<quest:re:{0}>".format(World.validation["quest"].pattern), callback=here)
    rv.route("/<quest:re:{0}>/move/<destination:re:{1}>".format(
        World.validation["quest"].pattern, World.validation["location"].pattern
    ), callback=move, method="POST")
    rv.route("/css/<filepath:path>", callback=serve_css)
    rv.route("/svg/<filepath:path>", callback=serve_svg)
    rv.world = World()

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
