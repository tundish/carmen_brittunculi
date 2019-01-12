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
from collections import deque
from collections import namedtuple
import logging
import random

from carmen.types import Compass
from carmen.types import Location
from carmen.types import Spot
from carmen.types import Visibility


class Clock:

    tick = None

    def __init__(self, period=1, stop=0):
        self.period = period
        self.stop = stop
        self.turn = None

    @classmethod
    async def next_event(cls, name="tick"):
        condition = getattr(cls, name, None)
        if condition and await condition.acquire():
            await condition.wait()
            condition.release()

    async def __call__(self, session, loop=None):
        log = logging.getLogger(
            "{0!s}.{1}".format(session.uid, self.__class__.__name__)
        )
        if Clock.tick is None:
            Clock.tick = asyncio.Condition(loop=loop)

        self.turn = 1
        while self.turn != self.stop:
            log.info(self.turn)
            await asyncio.sleep(self.period, loop=loop)
            if await Clock.tick.acquire():
                Clock.tick.notify_all()
                Clock.tick.release()
            self.turn += 1


class Angel:

    Move = namedtuple("Move", ["entity", "vector", "hop"])

    @staticmethod
    def locate(finder, actor):
        where = actor.get_state(Spot)
        return next((
            i for i in finder.ensemble()
            if isinstance(i, Location) and i.get_state(Spot) == where),
            None
        )

    @staticmethod
    def moves(finder, actor, destination, maxlen=20):
        here = actor.get_state(Spot)
        location = Angel.locate(finder, actor)
        route = finder.route(location, destination, maxlen=maxlen) or []
        for hop in route:
            spot = hop.get_state(Spot)
            vector = spot.value - here.value
            yield Angel.Move(actor, vector, hop)
            here = spot

    @staticmethod
    def visit(finder, target, options, maxlen=20):
        def hops(locn):
            route = finder.route(target, locn, maxlen)
            return len(route) if route is not None else maxlen + 1

        return next(iter(sorted(options, key=hops)), None)

    def __init__(self, actor, options):
        self.actor = actor
        self.options = options
        self.actions = deque([])

    async def __call__(self, session, loop=None):
        log = logging.getLogger(
            "{0!s}.{1}".format(session.uid, self.__class__.__name__)
        )
        if not hasattr(self.actor, "_lock"):
            self.actor._lock = asyncio.Lock(loop=loop)

        while True:
            try:
                await self.actor._lock.acquire()

                if self.actions:
                    move = self.actions.popleft()
                    move.entity.set_state(move.hop.get_state(Spot))
                    log.info("{0} goes {1} to {2.label}".format(
                        "{0.actor.name.firstname} {0.actor.name.surname}".format(self)
                        if move.entity is self.actor
                        else move.entity.label,
                        Compass.legend(move.vector),
                        move.hop
                    ))

                else:
                    player = session.cache.get("player", self.actor)
                    log.info("{0.actor.name.firstname} {0.actor.name.surname} tracks {1.name.firstname}".format(self, player))
                    location = self.visit(
                        session.finder,
                        self.locate(session.finder, player),
                        self.options
                    )
                    log.info("{0.actor.name.firstname} {0.actor.name.surname} chooses {1.label}".format(
                        self, location
                    ))
                    self.actions.extend(self.moves(session.finder, self.actor, location))

                await Clock.next_event()

            finally:
                self.actor._lock.release()
