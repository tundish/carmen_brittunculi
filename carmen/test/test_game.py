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

from collections.abc import Callable
import copy
import unittest

from turberfield.dialogue.performer import Performer
from turberfield.utils.misc import group_by_type

from carmen.logic import associations
from carmen.logic import episodes
from carmen.main import Game
from carmen.types import Player
from carmen.types import Spot
from carmen.types import Time

class Episode01Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.asscns = associations()
        cls.ensemble = list(cls.asscns.ensemble()) + [
            Player(name="Player").set_state(Spot.grid_1407).set_state(Time.eve_predawn)
        ]
        cls.dialogue = copy.deepcopy(episodes)
        cls.characters = {
            k.__name__: v for k, v in group_by_type(cls.ensemble).items()
        }
        cls.performer = Performer(cls.dialogue, cls.ensemble)

    def setUp(self):
        self.assertEqual(45, len(self.ensemble))
        (self.folder, self.index, self.script, self.selection,
         self.interlude) = self.performer.next(
            self.dialogue, self.ensemble, strict=True, roles=1
        )

    def tearDown(self):
        if isinstance(self.interlude, Callable):
            metadata = self.interlude(
                self.folder, self.index, self.ensemble,
                session=Game.Session(None, None, None, self.asscns, None)
            )
            self.assertIn(metadata, (None, self.folder.metadata))

    def test_001(self):
        self.assertEqual(
            next(iter(self.asscns.search(label="Kitchen"))).get_state(Spot),
            self.asscns.search(_name="Maer Catrine Cadi Ingenbrettar").pop().get_state(Spot)
        )

        list(self.performer.run())
        self.assertTrue(
            self.performer.script.fP.endswith("wood/enter.rst"),
            self.performer.script.fP
        )
        self.assertEqual(1, len(self.performer.shots))
        self.assertEqual("waking", self.performer.shots[-1].name)
