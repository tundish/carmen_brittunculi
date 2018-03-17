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

import enum
import string

from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Persona
from turberfield.dialogue.types import Stateful


class Visibility(EnumFactory, enum.Enum):
    hidden = 0
    visible = 1

class Speech(EnumFactory, enum.Enum):
    overheard = "overheard"
    studied = "studied"
    unspoken = "unspoken"
    spoken = "spoken"
    ignored = "ignored"
    repeated = "repeated"

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
class Location(Stateful, DataObject): pass
