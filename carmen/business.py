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
from collections import Counter
from collections import deque
from collections import namedtuple
from enum import Enum
import logging
import sys

import carmen.logic
from carmen.types import Compass
from carmen.types import DataObject
from carmen.types import Location
from carmen.types import Persona
from carmen.types import Spot
from carmen.types import Stateful

class Business:

    def __init__(self, actor, locations=None, operations=None):
        self.actor = actor
        self.locations = deque(locations or [])
        self.operations = deque(operations or [])
        self.log = logging.getLogger("business")

    def claim_resources(self, finder):
        if not hasattr(self.actor, "_lock"):
            self.actor._lock = asyncio.Lock(loop=loop)

        for i in finder.gather(self.locations, types=[Inventory]):
            i._business = self
            yield i

    async def __call__(self, finder, loop=None):

        for i in self.claim_resources(finder):
            self.log.info("{0} claimed by {1._name}".format(i, self.actor))

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
                    elif isinstance(act, Transfer):
                        if act.quantity:
                            act.source.contents[act.commodity] -= act.quantity
                            act.destination.contents[act.commodity] += act.quantity
                            self.log.info("{0.label} takes {1:0.3f} Kg {2.label}".format(
                                act.destination,
                                act.commodity.material.value * act.quantity,
                                act.commodity
                            ))
                            op.memory.append(act.destination.contents.copy())
                    await asyncio.sleep(0.1, loop=loop)
            finally:
                self.actor._lock.release()

            self.operations.rotate(-1)

    def deliver(self, finder, op):
        # Travel to nearest business location
        here = self.actor.get_state(Spot)
        options = {abs(i.get_state(Spot).value - here.value): i for i in self.locations}
        location = options[min(options)]
        yield from self.transport(finder, location)

        # Fill inventory from source
        resources = finder.gather([location], types=[Inventory], _business=self)
        sources = [i for i in resources if not i.mobility]
        carts = [i for i in resources if i.mobility]

        yield from self.transfer(sources, carts, op.objects)

        # Travel to destination
        destination = next(iter(op.locations))
        yield from self.transport(finder, destination)

        # Unload inventory to sink
        resources = finder.gather([destination], types=[Inventory])
        warehouses = [i for i in resources if not i.mobility]
        carts = [i for i in resources if i.mobility]
        yield from self.transfer(carts, warehouses, op.objects)

        # Travel back to nearest business location
        here = self.actor.get_state(Spot)
        options = {abs(i.get_state(Spot).value - here.value): i for i in self.locations}
        location = options[min(options)]
        yield from self.transport(finder, location)

    def resources(self, finder, locations, types=[Inventory], **kwargs):
        return [
            i
            for locn in locations
            for i in finder.search(**kwargs)
            if isinstance(i, tuple(types)) and i.get_state(Spot) == locn.get_state(Spot)
        ]

    @staticmethod
    def transfer(sources, destinations, materials=[object]):
        for dstn in destinations:
            space = dstn.capacity - sum(dstn.contents.values())
            for src in sources:
                while space > 0:
                    cargo = src.contents.copy()
                    for material, quantity in cargo.items():
                        if not isinstance(material, materials):
                            continue
                        load = min(space, quantity)
                        yield Transfer(src, material, load, dstn)
                        space -= load
                    else:
                        break

    def transport(self, finder, destination=None):
        here = self.actor.get_state(Spot)
        location = next(
            i for i in finder.ensemble()
            if isinstance(i, Location) and i.get_state(Spot) == here
        )
        containers = finder.gather([location], mobility=1, _business=self)
        route = finder.route(location, destination, maxlen=20)
        for hop in route:
            spot = hop.get_state(Spot)
            vector = spot.value - here.value
            yield Move(self.actor, vector, hop)
            yield from (Move(i, vector, hop) for i in containers)
            here = spot
