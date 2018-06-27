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

from collections import namedtuple
from enum import Enum

class Clock(Enum):

    midnight = 0


class Motivator:

    Move = namedtuple("Move", ["entity", "vector", "hop"])

    def __init__(self, actor):
        self.actor = actor

    def transport(self, finder, destination=None):
        here = self.actor.get_state(Spot)
        location = next(
            i for i in finder.ensemble()
            if isinstance(i, Location) and i.get_state(Spot) == here
        )
        route = finder.route(location, destination, maxlen=20)
        for hop in route:
            spot = hop.get_state(Spot)
            vector = spot.value - here.value
            yield Move(self.actor, vector, hop)
            here = spot

