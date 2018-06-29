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
from collections import namedtuple
from enum import Enum
import logging

Drama = namedtuple("Drama", ["entities", "memory"])
Affinity = namedtuple("Affinity", Drama._fields)

class Clock:

    period = 15
    tick = None

    async def __call__(self, name, loop=None):
        log = logging.getLogger(name)
        if Clock.tick is None:
            Clock.tick = asyncio.Condition(loop=loop)

        while True:
            await asyncio.sleep(Clock.period, loop=loop)
            if await Clock.tick.acquire():
                Clock.tick.notify_all()
                Clock.tick.release()

class Motivator:

    Move = namedtuple("Move", ["entity", "vector", "hop"])

    def __init__(self, actor, finder, *args):
        self.actor = actor
        self.finder = finder
        self.dramas = args

    def transport(self, destination=None):
        here = self.actor.get_state(Spot)
        location = next(
            i for i in self.finder.ensemble()
            if isinstance(i, Location) and i.get_state(Spot) == here
        )
        route = self.finder.route(location, destination, maxlen=20)
        for hop in route:
            spot = hop.get_state(Spot)
            vector = spot.value - here.value
            yield Move(self.actor, vector, hop)
            here = spot

    async def __call__(self, name, loop=None):
        log = logging.getLogger(name)

        if not hasattr(self.actor, "_lock"):
            self.actor._lock = asyncio.Lock(loop=loop)

        while True:

            try:
                await self.actor._lock.acquire()
                log.info(self.dramas)

                if Clock.tick and await Clock.tick.acquire():
                    await Clock.tick.wait()
                    Clock.tick.release()
            finally:
                self.actor._lock.release()
