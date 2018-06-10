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

class Visibility(EnumFactory, enum.Enum):
    hidden = 0
    visible = 1

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
    def bearing(cls, val, offset=0):
        keys, values = zip(*cls.rose.items())
        if isinstance(val, complex):
            phase = 180 * Decimal(cmath.phase(val)) / Decimal(cmath.pi)
            if phase <= 90:
                return 90 - phase - offset
            elif phase <= 180:
                return 270 + (180 - phase) - offset
            elif phase <= 270:
                return 180 + (270 - phase) - offset
            else:
                return 90 + 360 - phase - offset
        else:
            return val - offset

    @classmethod
    def legend(cls, val):
        offset = Decimal(180) / (len(cls.rose) - 1)
        val = cls.bearing(val, offset)
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
            (2, 3), (7, 3), (11, 2), (16, 3), (20, 3),
            (5, 5), (7, 6), (11, 6), (16, 5), (20, 5),
            (5, 7), (18, 7),
            (8, 8), (11, 9), (15, 8),
            (6, 10), (16, 10), (20, 10),
            (2, 11), (9, 11), (11, 11), (14, 11),
            (2, 14), (7, 14), (11, 13), (11, 15), (16, 14), (21, 14),
            (3, 18), (7, 18), (10, 17), (14, 17), (17, 17), (21, 17)
        )
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
class Marker(Stateful, DataObject): pass


Assembly.register(Spot)
