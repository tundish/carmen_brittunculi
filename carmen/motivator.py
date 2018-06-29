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
from enum import Enum
import logging

from carmen.types import Location
from carmen.types import Spot

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
        self.dramas = deque(args)
        self.actions = deque([])

    def travel(self, destination, maxlen=20):
        here = self.actor.get_state(Spot)
        location = next(
            i for i in self.finder.ensemble()
            if isinstance(i, Location) and i.get_state(Spot) == here
        )
        route = self.finder.route(location, destination, maxlen=maxlen)
        for hop in route:
            spot = hop.get_state(Spot)
            vector = spot.value - here.value
            yield Motivator.Move(self.actor, vector, hop)
            here = spot

    async def __call__(self, name, loop=None):
        log = logging.getLogger(name)

        if not hasattr(self.actor, "_lock"):
            self.actor._lock = asyncio.Lock(loop=loop)

        while True:

            try:
                await self.actor._lock.acquire()
                if self.actions:
                    act = self.actions.pop()
                    log.info(act)
                    if isinstance(act, Motivator.Move):
                        act.entity.set_state(act.hop.get_state(Spot))
                        log.info("{0} goes {1} to {2.label}".format(
                            "{0.actor.name.firstname} {0.actor.name.surname}".format(self)
                            if act.entity is self.actor
                            else act.entity.label,
                            Compass.legend(act.vector),
                            act.hop
                        ))
                else:
                    drama = self.dramas and self.dramas[-1]
                    if drama:
                        log.info(drama)
                        if isinstance(drama, Affinity):
                            here = self.actor.get_state(Spot)
                            options = {abs(i.get_state(Spot).value - here.value): i for i in drama.entities}
                            location = options[min(filter(None, options))]
                            log.info(location)
                            self.actions.extend(self.travel(location))
                            log.info(self.actions)

                        self.dramas.rotate(1)

                if Clock.tick and await Clock.tick.acquire():
                    await Clock.tick.wait()
                    Clock.tick.release()
            finally:
                self.actor._lock.release()
