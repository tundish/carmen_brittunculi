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
import itertools
import logging
import operator
import sys

import carmen.logic
from carmen.types import Compass
from carmen.types import DataObject
from carmen.types import Location
from carmen.types import Persona
from carmen.types import Spot
from carmen.types import Stateful
from carmen.types import Travel
from carmen.types import Via

class Volume(Enum):

    infinity = float("inf")
    load = 2
    heap = 1
    cubic_metre = 1
    pile = 25e-2
    box = 128e-3
    barrel = 128e-3
    keg = 64e-3
    sack = 32e-3
    slab = 24e-3
    case = 16e-3
    bundle = 8e-3
    bottle = 1e-3
    litre = 1e-3
    pack = 5e-4
    zero = 0

class Material(Enum):
    # Kg / m ^ 3
    limestone = 1800
    potato = 1060
    silver = 10490

Commodity = namedtuple("Commodity", ["label", "description", "volume", "material"])
SilverCoin = namedtuple("SilverCoin", Commodity._fields)

class NPC(Stateful, Persona): pass

class Inventory(Stateful, DataObject):

    def __init__(self, capacity, **kwargs):
        self.capacity = capacity
        self.contents = Counter()
        super().__init__(**kwargs)

class Business:

    def __init__(self, actor, locations=None):
        self.actor = actor
        self.locations = locations or []
        self.log = logging.getLogger("business")

    async def __call__(self, finder, loop=None):
        if not hasattr(self.actor, "_lock"):
            self.actor._lock = asyncio.Lock(loop=loop)

        while True:
            destination = self.locations[0]
            for spot in self.travel(finder, destination):
                self.actor.set_state(spot)
            self.locations.rotate(-1)

    def travel(self, finder, destination=None):
        here = self.actor.get_state(Spot)
        location = next(i for i in finder.ensemble() if isinstance(i, Location) and i.get_state(Spot) == here)
        route = finder.route(location, destination, maxlen=20)
        for hop in route:
            spot = hop.get_state(Spot)
            yield spot
            self.log.info("{0.actor.name.firstname} {0.actor.name.surname} goes {1} to {2.label}".format(
                self, Compass.legend(spot.value - here.value), hop
            ))
            here = spot

rf = carmen.logic.associations()

rf.register(
    Travel.intention,
    NPC(name="Civis Anatol Ant Bospor").set_state(
        next(iter(rf.search(label="Common house"))).get_state(Spot)
    ),
    next(iter(rf.search(label="Marsh")))
)

rf.register(
    Travel.refusal,
    NPC(name="Maer Catrine Cadi Ingenbrettar").set_state(
        next(iter(rf.search(label="Common house"))).get_state(Spot)
    ),
    next(iter(rf.search(label="Quarry")))
)

rf.register(
    None,
    Inventory(label="Stone", capacity=Volume.infinity).set_state(
        next(iter(rf.search(label="Quarry"))).get_state(Spot)
    ),
)

rf.register(
    None,
    Inventory(label="Cart", capacity=Volume.load).set_state(
        next(iter(rf.search(label="Quarry"))).get_state(Spot)
    ),
)

rf.register(
    None,
    Inventory(label="Market", capacity=Volume.infinity).set_state(
        next(iter(rf.search(label="Marsh"))).get_state(Spot)
    ),
)

# Businesses claim actors and lock them while they are in use
businesses = [
    Business(
        next(iter(rf.search(_name="Civis Anatol Ant Bospor"))),
        locations=deque([
            next(iter(rf.search(label="Quarry"))),
            next(iter(rf.search(label="Marsh")))
        ])
    )
]

print(*rf.ensemble(), sep="\n")

logging.basicConfig(level=logging.INFO)
loop = asyncio.SelectorEventLoop()
asyncio.set_event_loop(None)

for business in businesses:
    loop.create_task(business(rf, loop))

loop.run_forever()
loop.close()
