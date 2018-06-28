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

class Motivator:

    Move = namedtuple("Move", ["entity", "vector", "hop"])

    def __init__(self, actor, finder, *args):
        self.log = logging.getLogger("motivator")
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

    async def __call__(self, loop=None):

        if not hasattr(self.actor, "_lock"):
            self.actor._lock = asyncio.Lock(loop=loop)

        while True:

            try:
                await self.actor._lock.acquire()

                op = self.operations[0]

                if isinstance(op, Delivering):
                    actions = self.deliver(finder, op)

                for act in actions:
                    if isinstance(act, Move):
                        act.entity.set_state(act.hop.get_state(Spot))
                        self.log.info("{0} goes {1} to {2.label}".format(
                            "{0.actor.name.firstname} {0.actor.name.surname}".format(self)
                            if act.entity is self.actor
                            else act.entity.label,
                            Compass.legend(act.vector),
                            act.hop
                        ))
                    await asyncio.sleep(0, loop=loop)
            finally:
                self.actor._lock.release()
