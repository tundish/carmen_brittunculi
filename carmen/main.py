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

import asyncio
import argparse
from collections import deque
from collections import namedtuple
import functools
import itertools
import logging
import sys
import uuid

from aiohttp import web
import bottle
import pkg_resources
from turberfield.dialogue.performer import Performer
from turberfield.utils.misc import log_setup

from carmen import __version__
from carmen.handler import Handler
import carmen.logic
from carmen.types import Compass
from carmen.types import Location
from carmen.types import Narrator
from carmen.types import Player
from carmen.types import Spot
from carmen.types import Time
from carmen.types import Visibility

MAX_FRAME_S = 21.3  # 8 bars at 90 BPM
DEFAULT_PORT = 8080
DEFAULT_PAUSE = 1.2
DEFAULT_DWELL = 0.3

class Game:

    sessions = {}

    Session = namedtuple("Session", ["uid", "cache", "frames", "finder", "workers"])

    @staticmethod
    def session(name, loop=None):
        loop = loop or asyncio.get_event_loop()
        finder = carmen.logic.associations()
        activities = carmen.logic.activities(finder)
        start = next(iter(finder.search(label="Green lane")))
        player = Player(name=name).set_state(start.get_state(Spot))
        player.set_state(Time.day_sunrise)
        finder.register(None, player)
        uid = uuid.uuid4()
        rv = Game.Session(
            uid, {"player": player}, deque([]), finder,
            [loop.create_task(i(str(uid), loop=loop)) for i in activities]
        )
        Game.sessions[uid] = rv
        return rv

    @staticmethod
    def spot(session):
        """Return the player's spot."""
        player = session.cache.setdefault(
            "player",
            next(i for i in session.finder.lookup if isinstance(i, Player))
        )
        return player.get_state(Spot)

    @staticmethod
    def moves(session, spot=None):
        """Return the location and available moves from a spot."""
        spot = spot or Game.spot(session)

        locn = next(
            i for i in session.finder.lookup
            if isinstance(i, Location) and i.get_state(Spot) == spot
        )
        moves = [
            (Compass.legend(k), v)
            for k, v in session.finder.navigate(locn).items()
        ]
        return locn, moves

    @staticmethod
    def entities(session, spot=None):
        """Return the entities available around a spot."""
        spot = spot or Game.spot(session)

        return [
            i for i in session.finder.ensemble()
            if i.get_state(Spot) == spot
            or i.get_state(Visibility) in (Visibility.indicated, Visibility.new)
            or isinstance(i, Narrator)
        ]

    @staticmethod
    def frame(session, entities):
        """Return the next frame of action for presentation handling."""
        if not session.frames:
            performer = Performer(carmen.logic.episodes, entities)
            folder, index, script, selection, interlude = performer.next(
                carmen.logic.episodes, entities
            )
            scene = itertools.chain(
                performer.run(react=False),
                [functools.partial(
                    interlude, folder, index, entities,
                    **session.cache
                )] if interlude else []
            )
            session.frames.extend(Handler.frames(scene, dwell=0.3, pause=1))

        return session.frames.popleft()

async def get_start(request):
    return web.Response(
        text=bottle.template(
            pkg_resources.resource_string("carmen", "templates/session.tpl").decode("utf8"),
            validation=Handler.validation,
            refresh=None
        ),
        content_type="text/html"
    )

async def post_start(request):
    log = logging.getLogger("carmen.main.start")
    data = await request.post()
    name = data["playername"]
    email = data["email"]
    if not Handler.validation["name"].match(name):
        raise web.HTTPUnauthorized(reason="User input invalid name.")

    if not Handler.validation["email"].match(email):
        log.warning("User input invalid email.")
    else:
        log.info("Email offered: {0}".format(email))

    session = Game.session(name)
    log.info("Player {0} created session {1.uid!s}".format(name, session))
    raise web.HTTPFound("/{0.uid.hex}".format(session))

async def here(request):
    log = logging.getLogger("carmen.main.here")
    uid = uuid.UUID(hex=request.match_info["session"])

    session = Game.sessions[uid]
    locn, moves = Game.moves(session)
    spot = locn.get_state(Spot)
    player = session.cache.get("player")

    entities = Game.entities(session, spot)
    frame = Game.frame(session, entities)
    player.set_state(player.get_state(int) + 1)
    metadata = Handler.react(session, frame)

    refresh = sum(session.frames[-1][1:3]) if session.frames else MAX_FRAME_S
    n_items = len([i for i in session.finder.ensemble() if i.get_state(Spot) == Spot.pockets])

    return web.Response(
        text=bottle.template(
            pkg_resources.resource_string("carmen", "templates/here.tpl").decode("utf8"),
            here=locn,
            moves=sorted(moves),
            items=n_items,
            session=session,
            frame=frame,
            ordinal=player.get_state(int),
            refresh=refresh
        ),
        content_type="text/html"
    )

async def move(request):
    log = logging.getLogger("carmen.main.move")
    session_uid = uuid.UUID(hex=request.match_info["session"])
    try:
        session = Game.sessions[session_uid]
    except KeyError:
        raise web.HTTPUnauthorized(reason="Session {0!s} not found.".format(session_uid))

    locn, moves = Game.moves(session)
    dest_uid = uuid.UUID(hex=request.match_info["destination"])
    try:
        destn = next(i for i in dict(moves).values() if i.id == dest_uid)
        session.cache["player"].set_state(destn.get_state(Spot))
        locn.set_state(Visibility.visible)
        destn.set_state(Visibility.detail)
        log.info("Player {0} moved to {1}".format(
            session.cache["player"], destn))
    except Exception as e:
        log.exception(e)
    finally:
        raise web.HTTPFound("/{0.hex}".format(session_uid))

def build_app(args):
    app = web.Application()
    try:
        add_routes = app.add_routes
        add_static = app.add_static
    except AttributeError:
        # Aiohttp v2
        add_routes = app.router.add_routes
        add_static = app.router.add_static

    add_routes([
        web.get("/", get_start),
        web.post("/", post_start),
        web.get("/{{session:{0}}}".format(Handler.validation["session"].pattern), here),
        web.post("/{{session:{0}}}/move/{{destination:{1}}}".format(
            Handler.validation["session"].pattern, Handler.validation["location"].pattern
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
    app.game = Game()

    bottle.TEMPLATE_PATH.append(
        pkg_resources.resource_filename("carmen", "templates")
    )

    return app

def main(args):
    log = logging.getLogger(log_setup(args, ""))

    app = build_app(args)

    # TODO: Migrate to aiohttp v3 and use
    # https://docs.aiohttp.org/en/stable/web_advanced.html#background-tasks
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    handler = app.make_handler()
    f = loop.create_server(handler, "0.0.0.0", args.port)
    srv = loop.run_until_complete(f)

    log.info("Serving on {0[0]}:{0[1]}".format(srv.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()

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
