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
import logging
import re
import sys
import uuid

from aiohttp import web
import bottle
import pkg_resources
from turberfield.dialogue.performer import Performer
from turberfield.utils.misc import log_setup

from carmen import __version__
import carmen.logic
from carmen.types import Coin
from carmen.types import Compass
from carmen.types import Location
from carmen.types import Player
from carmen.types import Marker
from carmen.types import Spot
from carmen.types import Via
from carmen.utils import Scenery

DEFAULT_PORT = 8080
DEFAULT_PAUSE = 1.2
DEFAULT_DWELL = 0.3

bottle.TEMPLATE_PATH.append(
    pkg_resources.resource_filename("carmen", "templates")
)

class World:

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

        locn = next(
            i for i in asscns.lookup
            if isinstance(i, Location) and i.get_state(Spot) == spot
        )
        moves = [
            (Compass.legend(k), v)
            for k, v in asscns.navigate(locn).items()
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

async def get_start(request):
    return web.Response(
        text=bottle.template(
            pkg_resources.resource_string("carmen", "templates/quest.tpl").decode("utf8"),
            validation=World.validation,
        ),
        content_type="text/html"
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

    width, height = 560, 400
    pitch = (16, 16)
    cell = (32, 32)
    # TODO: Do select. Use values.
    cast = {}
    coin = next((i for i in cast.values() if isinstance(i, Coin)), None)
    marker = next((i for i in cast.values() if isinstance(i, Marker)), None)
    return bottle.template(
        pkg_resources.resource_string("carmen", "templates/here.tpl").decode("utf8"),
        extent=(width + cell[0] - pitch[0], height + cell[1] - pitch[1]),
        leaves=Scenery.forest(width, height, pitch=pitch),
        # leaves=[],
        here=locn,
        lines=list(scene),
        moves=sorted(moves),
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

def build_app(args):
    app = web.Application()
    try:
        add_routes = app.add_routes
        add_static = app.add_static
    except AttributeError:
        # Asiohttp v2
        add_routes = app.router.add_routes
        add_static = app.router.add_static

    add_routes([
        web.get("/", get_start),
        web.post("/", post_start),
        web.get("/{{quest:{0}}}".format(World.validation["quest"].pattern), here),
        web.post("/{{quest:{0}}}/move/{{destination:{1}}}".format(
            World.validation["quest"].pattern, World.validation["location"].pattern
        ), move),
    ])

    add_static(
        "/css/",
        pkg_resources.resource_filename("carmen", "static/css")
    )
    add_static(
        "/svg/",
        pkg_resources.resource_filename("carmen", "static/svg")
    )
    app.world = World()

    return app

def main(args):
    log = logging.getLogger(log_setup(args, "carmen"))

    app = build_app(args)

    log.info("Starting server...")
    web.run_app(app, host="0.0.0.0", port=args.port)

def parser(description=__doc__):
    rv = argparse.ArgumentParser(
        description,
        fromfile_prefix_chars="@"
    )
    rv.add_argument(
        "--version", action="store_true", default=False,
        help="Print the current version number.")
    rv.add_argument(
        "-v", "--verbose", required=False,
        action="store_const", dest="log_level",
        const=logging.DEBUG, default=logging.INFO,
        help="Increase the verbosity of output.")
    rv.add_argument(
        "--log", default=None, dest="log_path",
        help="Set a file path for log output.")
    rv.add_argument(
        "--port", type=int, default=DEFAULT_PORT,
        help="Specify the port number [{}].".format(
            DEFAULT_PORT
        )
    )
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
