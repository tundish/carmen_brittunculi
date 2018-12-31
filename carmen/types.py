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
import string

from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Persona
from turberfield.dialogue.types import Player # noqa
from turberfield.dialogue.types import Stateful
from turberfield.utils.assembly import Assembly

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

class Wants(EnumFactory, enum.Enum):
    nothing = 0
    needs = 1
    needs_warmth = 2
    needs_food = 3
    needs_sleep = 4

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

class Speech(EnumFactory, enum.Enum):
    overheard = "overheard"
    studied = "studied"
    unspoken = "unspoken"
    spoken = "spoken"
    ignored = "ignored"
    repeated = "repeated"


Spot = enum.Enum(
    "Spot", [
        ("grid_{0:02}{1:02}".format(*point), complex(*point))
        for point in (
            (15, 0), (13, 2), (11, 4), (8, 4), (8, 13), (13, 6),
            (9, 6), (9, 8), (9, 9), (13, 8), (14, 7),
            (14, 13), (8, 16), (11, 16), (14, 16),

            # master branch
            (2, 3), (7, 3), (11, 2), (16, 3), (20, 3),
            (5, 5), (7, 6), (11, 6), (16, 5), (20, 5),
            (5, 7), (18, 7),
            (8, 8), (11, 9), (15, 8),
            (6, 10), (16, 10), (20, 10),
            (2, 11), (9, 11), (11, 11), (14, 11),
            (2, 14), (7, 14), (11, 13), (11, 15), (16, 14), (21, 14),
            (3, 18), (7, 18), (10, 17), (14, 17), (17, 17), (21, 17)
        )
    ] + [
        ("pockets", None)
    ],
    module=__name__,
    type=EnumFactory
)

class Travel(EnumFactory, enum.Enum):
    refusal = "refusal"
    intention = "intention"
    departure = "departure"
    transit = "transit"
    arrival = "arrival"

class Via(EnumFactory, enum.Enum):
    block = 0
    forwd = 1
    bckwd = 2
    bidir = 3

class Phrase:

    """
    Allows on-the-fly creation of singleton classes to represent spoken phrases.
    The instance object is stateful, so can be an entity in a dialogue file.

    """

    _table = {
        ord(c): val
        for seq, val in ((string.punctuation, None), (string.whitespace, " "))
        for c in seq
    }

    @staticmethod
    def build(text, html=None):

        @classmethod
        def instance(cls):
            if getattr(cls, "_instance", None) is None:
                cls._instance = cls()
            return cls._instance

        html = html or text
        return type(
            Phrase.class_name(text),
            (Stateful,),
            {"text": text, "html": html, "instance": instance}
        )

    @staticmethod
    def class_name(text):
        sane = text.lower().translate(Phrase._table)
        return "".join(i.capitalize() for i in sane.split())

class Narrator(Stateful): pass
class Character(Stateful, Persona): pass
class Coin(Stateful, DataObject): pass
class Location(Stateful, DataObject): pass
class CubbyFruit(Stateful): pass


Assembly.register(Spot)
