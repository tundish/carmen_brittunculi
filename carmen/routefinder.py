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

    def moves(self, locn):
        """
        Refactor for reuse
        """
        spot = locn.get_state(Spot)
        neighbours = self.match(
            locn,
            forward=[Via.bidir, Via.forwd],
            reverse=[Via.bidir, Via.bckwd],
            predicate=lambda x: isinstance(x, Location)
        )
        moves = [
            (Compass.legend(i.get_state(Spot).value - spot.value), i)
            for i in neighbours
        ]
        return locn, moves

    def route(self, locn, dest, maxlen, visited=None):
        if (locn, dest) in self._cache:
            return self._cache[(locn, dest)]

        visited = set([]) if visited is None else set(visited)
        if locn == dest:
            return deque([], maxlen=maxlen)

        bearing = Compass.bearing(dest.get_state(Spot).value - locn.get_state(Spot).value)

        spot = locn.get_state(Spot)
        neighbours = self.match(
            locn,
            forward=[Via.bidir, Via.forwd],
            reverse=[Via.bidir, Via.bckwd],
            predicate=lambda x: isinstance(x, Location)
        )
        options = sorted(
            ((abs(Compass.bearing(i.get_state(Spot).value - spot.value) - bearing), i)
             for i in neighbours
             if i not in visited),
            key=operator.itemgetter(0)
        )
        while options:
            deviation, hop = options.pop(0)
            visited.add(hop)
            try:
                rv = deque(self.route(hop, dest, maxlen, frozenset(visited)))
            except TypeError:
                # rv is None
                continue

            if hop in rv:
                continue

            rv.appendleft(hop)

            if rv[-1] == dest:
                self._cache[(locn, dest)] = tuple(rv)
                return rv

            if len(rv) == maxlen:
                return None
        else:
            return None


