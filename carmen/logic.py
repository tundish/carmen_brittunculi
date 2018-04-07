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

import collections
import datetime
import itertools

from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.types import Player

from carmen import __version__ as version # noqa
from carmen.associations import Associations
from carmen.types import Location
from carmen.types import Spot
from carmen.types import Via

ides_of_march = datetime.date(396, 3, 1)

def associations():
    rv = Associations()
    rv.register(
        Via.bidir,
        Location(label="Grove of Hades").set_state(Spot.grid_0808),
        Location(label="Quarry path").set_state(Spot.grid_0610),
        Location(label="Brambly dell").set_state(Spot.grid_0507),
        Location(label="Common house").set_state(Spot.grid_1106),
        Location(label="North gate").set_state(Spot.grid_1109),
    )
    return rv

references = list(associations().ensemble()) + [Spot, Via]
