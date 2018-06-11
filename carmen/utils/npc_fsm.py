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
from enum import Enum
import functools
import itertools

import carmen.logic
from carmen.types import Compass
from carmen.types import Location
from carmen.types import Spot
from carmen.types import Via

@functools.lru_cache(maxsize=None)
def path(locn, dest, maxlen):
    print("Called: ", locn, dest, sep="\n")
    if locn == dest:
        return deque([], maxlen=maxlen)

    bearing = Compass.bearing(dest.get_state(Spot).value - locn.get_state(Spot).value)

    spot = locn.get_state(Spot)
    neighbours = asscns.match(
        locn,
        forward=[Via.bidir, Via.forwd],
        reverse=[Via.bidir, Via.bckwd],
        predicate=lambda x: isinstance(x, Location)
    )
    options = {
        abs(Compass.bearing(i.get_state(Spot).value - spot.value) - bearing): i
        for i in neighbours
    }
    for option in sorted(options.keys()):
        hop = options[option]
        rv = path(hop, dest, maxlen)
        print("Returned: ", rv)
        if rv is None or hop in rv:
            continue

        rv.appendleft(hop)

        if rv[-1] == dest:
            return rv

        if len(rv) == maxlen:
            return None

asscns = carmen.logic.associations()
locns = [i for i in asscns.ensemble() if isinstance(i, Location)]
for locn, dest in itertools.permutations(locns, r=2):
    print(
        "From {0.label} {1} to {2.label} {3}".format(
            locn, locn.get_state(Spot).value, dest, dest.get_state(Spot).value
        )
    )
    route = path(locn, dest, len(locns))
    print(*route, sep="\n")
    #input("Press return.")
