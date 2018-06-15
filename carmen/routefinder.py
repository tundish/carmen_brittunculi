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
from collections import OrderedDict
import operator

from carmen.associations import Associations
from carmen.types import Compass
from carmen.types import Location
from carmen.types import Spot
from carmen.types import Via

class Routefinder(Associations):

    def __init__(self):
        super().__init__()
        self._cache = {}

    def navigate(self, locn):
        spot = locn.get_state(Spot)
        neighbours = self.match(
            locn,
            forward=[Via.bidir, Via.forwd],
            reverse=[Via.bidir, Via.bckwd],
            predicate=lambda x: isinstance(x, Location)
        )
        return OrderedDict([(
            Compass.bearing(i.get_state(Spot).value - spot.value),
            i
        ) for i in neighbours])

    def route(self, locn, dest, maxlen, visited=None):
        if (locn, dest) in self._cache:
            return self._cache[(locn, dest)]

        visited = set([]) if visited is None else set(visited)
        if locn == dest:
            return deque([], maxlen=maxlen)

        bearing = Compass.bearing(dest.get_state(Spot).value - locn.get_state(Spot).value)
        moves = self.navigate(locn)
        options = sorted(
            ((abs(k - bearing), v) for k, v in moves.items() if v not in visited),
            key=operator.itemgetter(0)
        )

        while options:
            deviation, hop = options.pop(0)
            visited.add(hop)
            try:
                rv = deque(self.route(hop, dest, maxlen, frozenset(visited)))
                if hop in rv:
                    continue
                else:
                    self._cache[(hop, dest)] = tuple(rv)
                    rv.appendleft(hop)
            except TypeError:
                continue

            if len(rv) == maxlen:
                return None

            return rv
        else:
            return None

    def gather(self, locations, types=[object], **kwargs):
        return [
            i
            for locn in locations
            for i in self.search(**kwargs)
            if isinstance(i, tuple(types))
            and i.get_state(Spot) == locn.get_state(Spot)
        ]

