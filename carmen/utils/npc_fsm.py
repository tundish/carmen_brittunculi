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

from enum import Enum
import itertools

import carmen.logic
from carmen.types import Compass
from carmen.types import Location
from carmen.types import Spot
from carmen.types import Via

def path(locn, dest):
    bearing = Compass.bearing(dest - locn)
    return bearing

asscns = carmen.logic.associations()
locns = [i for i in asscns.ensemble() if isinstance(i, Location)]
for locn, dest in itertools.permutations(locns, r=2):
    rv = []
    bearing = Compass.bearing(dest.get_state(Spot).value - locn.get_state(Spot).value)
    pos = locn
    while pos != dest and len(rv) < len(locns):
        spot = pos.get_state(Spot)
        neighbours = asscns.match(
            pos,
            forward=[Via.bidir, Via.forwd],
            reverse=[Via.bidir, Via.bckwd],
            predicate=lambda x: isinstance(x, Location)
        )
        errors = {
            abs(Compass.bearing(i.get_state(Spot).value - spot.value) - bearing): i
            for i in neighbours
        }
        hop = errors[min(errors)]
        rv.append(hop)
    else:
        print(rv)
