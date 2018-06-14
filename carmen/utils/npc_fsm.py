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
    plenty = sys.maxsize
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

Commodity = namedtuple("Commodity", ["label", "description", "material"])

Potato = namedtuple("Potato", Commodity._fields)
SilverCoin = namedtuple("SilverCoin", Commodity._fields)
Stone = namedtuple("Stone", Commodity._fields)

Drama = namedtuple("Drama", ["objects", "locations", "memory"])
Buying = namedtuple("Buying", Drama._fields)
Selling = namedtuple("Selling", Drama._fields)
Collecting = namedtuple("Collecting", Drama._fields)
Delivering = namedtuple("Delivering", Drama._fields)

class NPC(Stateful, Persona): pass

class Inventory(Stateful, DataObject):

    def __init__(self, capacity, mobility=1, contents: Counter=None, **kwargs):
        self.capacity = getattr(capacity, "value", capacity)
        self.mobility = mobility
        self.contents = contents or Counter()
        super().__init__(**kwargs)

class Business:

    def __init__(self, actor, locations=None, operations=None):
        self.actor = actor
        self.locations = locations or []
        self.operations = operations or []
        self.log = logging.getLogger("business")

    async def __call__(self, finder, loop=None):
        if not hasattr(self.actor, "_lock"):
            self.actor._lock = asyncio.Lock(loop=loop)

        while True:
            # Travel to location
            destination = self.locations[0]
            for entity, vector, hop in self.transport(finder, destination):
                entity.set_state(hop.get_state(Spot))
                self.log.info("{0} goes {1} to {2.label}".format(
                    "{0.actor.name.firstname} {0.actor.name.surname}".format(self)
                    if entity is self.actor
                    else entity.label,
                    Compass.legend(vector),
                    hop
                ))

            # Fill inventory from source
            here = self.actor.get_state(Spot)
            location = next(i for i in finder.ensemble() if isinstance(i, Location) and i.get_state(Spot) == here)
            resources = self.resources(finder, [location])
            sources = [i for i in resources if not i.mobility]
            carts = [i for i in resources if i.mobility]

            for src, commodity, quantity, dstn in self.transfer(sources, carts, self.operations[0].objects):
                src.contents[commodity] -= quantity
                dstn.contents[commodity] += quantity
                self.log.info("{0.label} takes {1:0.3f} Kg {2.label}".format(
                    dstn, commodity.material.value * quantity, commodity
                ))

            # Travel to destination
            destination = self.locations[0]
            for entity, vector, hop in self.transport(finder, destination):
                entity.set_state(hop.get_state(Spot))
                self.log.info("{0} goes {1} to {2.label}".format(
                    "{0.actor.name.firstname} {0.actor.name.surname}".format(self)
                    if entity is self.actor
                    else entity.label,
                    Compass.legend(vector),
                    hop
                ))
                await asyncio.sleep(1, loop=loop)

            # Unload inventory to sink
            resources = self.resources(finder, [destination])
            warehouses = [i for i in resources if not i.mobility]
            carts = [i for i in resources if i.mobility]

            for src, commodity, quantity, dstn in self.transfer(carts, warehouses, self.operations[0].objects):
                src.contents[commodity] -= quantity
                dstn.contents[commodity] += quantity
                self.log.info("{0.label} takes {1:0.3f} Kg {2.label}".format(
                    dstn, commodity.material.value * quantity, commodity
                ))


            self.locations.rotate(-1)
            self.operations.rotate(-1)

    def resources(self, finder, locations, types=[Inventory]):
        claims = set(self.locations).intersection(set(locations))
        return [
            i
            for locn in claims
            for i in finder.ensemble()
            if isinstance(i, tuple(types))
            and i.get_state(Spot) == locn.get_state(Spot)
        ]

    @staticmethod
    def transfer(sources, destinations, materials):
        for dstn in destinations:
            space = dstn.capacity - sum(dstn.contents.values())
            for src in sources:
                while space > 0:
                    for material, quantity in src.contents.items():
                        load = min(space, quantity)
                        yield src, material, load, dstn
                        space -= load
                    else:
                        break

    def transport(self, finder, destination=None):
        here = self.actor.get_state(Spot)
        location = next(i for i in finder.ensemble() if isinstance(i, Location) and i.get_state(Spot) == here)
        entities = [i for i in finder.search(label="Cart") if i.get_state(Spot) == here]
        route = finder.route(location, destination, maxlen=20)
        for hop in route:
            spot = hop.get_state(Spot)
            vector = spot.value - here.value
            yield self.actor, vector, hop
            yield from ((i, vector, hop) for i in entities)
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
    Inventory(
        label="Stone",
        mobility=0,
        capacity=Volume.infinity,
        contents=Counter({
            Stone("Limestone", "Freshly quarried limestone", Material.limestone): Volume.plenty.value
        })
    ).set_state(
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
    Inventory(
        label="Market",
        mobility=0,
        capacity=Volume.infinity,
        contents=Counter({
            Potato("Potato", "Potatoes from market", Material.potato): Volume.plenty.value
        })
    ).set_state(
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
        ]),
        operations=deque([
            Delivering((Stone,), rf.search(label="Marsh"), deque([])),
            Delivering((Potato,), rf.search(label="Common house"), deque([])),
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
