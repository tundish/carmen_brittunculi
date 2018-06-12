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

from collections import deque
from collections import namedtuple
from enum import Enum
import itertools
import operator
import sys

import carmen.logic
from carmen.types import Compass
from carmen.types import Location
from carmen.types import Spot
from carmen.types import Via

class Volume(Enum):

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

print(Material.silver.value)

sys.exit(0)
asscns = carmen.logic.associations()
locns = [i for i in asscns.ensemble() if isinstance(i, Location)]
longest = (None, None, [])
for locn, dest in itertools.permutations(locns, r=2):
    print(
        "From {0.label} {1} to {2.label} {3}".format(
            locn, locn.get_state(Spot).value, dest, dest.get_state(Spot).value
        )
    )
    route = asscns.route(locn, dest, len(locns))
    if route is None:
        print("Can't find route for {0} to {1}".format(locn, dest))
    else:
        print(*route, sep="\n")
        if len(route) > len(longest[2]):
            longest = (locn, dest, route)
print("{0.label} -> {1.label}".format(*longest))
print(*longest[2], sep="\n")
