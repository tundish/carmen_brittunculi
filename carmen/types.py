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

import bisect
import cmath
from collections import deque
from collections import OrderedDict
from decimal import Decimal
import enum

from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Persona
from turberfield.dialogue.types import Player # noqa
from turberfield.dialogue.types import Stateful
from turberfield.utils.assembly import Assembly

from carmen import __version__ as version # noqa

class Stepper(enum.Enum):

    @classmethod
    def advance(cls, instance):
        """Return the next highest member of the enum class."""
        members = deque(cls)
        members.rotate(-instance.value - 1)
        return members[0]


class Time(EnumFactory, Stepper):
    eve_midnight = 0
    eve_night = 1
    eve_predawn = 2
    eve_dawn = 3
    day = 4
    day_sunrise = 4
    day_early = 5
    day_breakfast = 6
    day_morning = 7
    day_noon = 8
    day_lunch = 9
    day_afternoon = 10
    day_dinner = 11
    day_dusk = 12
    eve = 13
    eve_sunset = 13
    eve_evening = 14
    eve_supper = 15


class Visibility(EnumFactory, enum.Enum):
    hidden = 0
    visible = 1
    detail = 2
    indicated = 3
    new = 4


class Compass:

    rose = OrderedDict([
        (0, "North"),
        (45, "NorthEast"),
        (90, "East"),
        (135, "SouthEast"),
        (180, "South"),
        (225, "SouthWest"),
        (270, "West"),
        (315, "NorthWest"),
        (360, "North")
    ])

    @classmethod
    def bearing(cls, val: complex):
        phase = 180 * Decimal(cmath.phase(val)) / Decimal(cmath.pi)
        if phase <= 90:
            return 90 - phase
        elif phase <= 180:
            return 270 + (180 - phase)
        elif phase <= 270:
            return 180 + (270 - phase)
        else:
            return 90 + 360 - phase

    @classmethod
    def legend(cls, val):
        if isinstance(val, complex):
            val = cls.bearing(val)
        val -= Decimal(180) / (len(cls.rose) - 1)
        keys, values = zip(*cls.rose.items())
        pos = bisect.bisect_left(keys, val)
        return values[pos]


Spot = enum.Enum(
    "Spot", [
        ("grid_{0:02}{1:02}".format(*point), complex(*point))
        for point in (
            (2, 9), (2, 11), (3, 13), (3, 18), (6, 10), (6, 13), (7, 18), (8, 4),
            (8, 16), (9, 6), (9, 8), (9, 10), (9, 11), (9, 13), (10, 17), (11, 4),
            (11, 9), (11, 11), (11, 13), (11, 16), (12, 5), (12, 6), (12, 8), (13, 2), (13, 10),
            (14, 13), (14, 16), (15, 0), (15, 8), (16, 3), (16, 5), (16, 9),
            (16, 10), (16, 14), (17, 17), (18, 7), (20, 3), (20, 5), (20, 10), (21, 14),
            (21, 17)
        )
    ] + [
        ("grid", True),
        ("pockets", False)
    ],
    module=__name__,
    type=EnumFactory
)

class Via(EnumFactory, enum.Enum):
    block = 0
    forwd = 1
    bckwd = 2
    bidir = 3

class Narrator(Stateful): pass
class Character(Stateful, Persona): pass
class Innkeeper(Character): pass
class Merchant(Character): pass
class Priest(Character): pass
class Woodsman(Character): pass

class Collectable(Stateful): pass
class Bowl(Collectable): pass
class Coin(Collectable, DataObject): pass
class CubbyFruit(Collectable): pass

class Location(Stateful, DataObject): pass
class Exterior(Location): pass
class Interior(Location): pass
class Dwelling(Interior): pass
class Settlement(Exterior): pass
class Court(Exterior): pass
class Sanctum(Interior): pass
class Pit(Exterior): pass
class Workings(Interior): pass
class Forest(Interior): pass
class Heath(Exterior): pass
class Woodland(Exterior): pass


Assembly.register(Spot)
