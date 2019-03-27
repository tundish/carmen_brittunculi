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

import asyncio
import unittest

from carmen.agents import Clock
from carmen.agents import Angel
from carmen.logic import routines
from carmen.logic import associations
from carmen.logic import episodes
from carmen.logic import Rules
from carmen.main import Game
from carmen.types import Location
from carmen.types import Narrator
from carmen.types import Time
from carmen.types import Via

class TestRules(unittest.TestCase):

    def test_advance_time(self):
        for n, i in enumerate(Time):
            with self.subTest(val=i):
                self.assertEqual(n, i.value)
                self.assertEqual((n + 1) % len(Time), Time.advance(i).value)

    def test_rules(self):
        self.assertEqual(10, len(Rules.zone), "Map TBD")

class TestDialogue(unittest.TestCase):

    def test_folder(self):
        self.assertEqual(55, len(episodes[0].paths))

    def test_cast(self):
        asscns = associations()
        self.assertTrue(len([i for i in asscns.ensemble() if isinstance(i, Narrator)]))

class TestNavigation(unittest.TestCase):

    def setUp(self):
        self.a = associations()

    def test_new_world(self):
        loop = asyncio.new_event_loop()
        try:
            session = Game.session("Stig", loop=loop)
            self.assertEqual(41, len([i for i in session.finder.lookup if isinstance(i, Location)]))
        finally:
            loop.close()

    def test_associations(self):
        locn = next(iter(self.a.search(label="Grove of Hades")))
        neighbours = self.a.match(
            locn,
            forward=[Via.bidir, Via.forwd],
            reverse=[Via.bidir, Via.bckwd],
            predicate=lambda x: isinstance(x, Location)
        )
        self.assertEqual(2, len(neighbours))

class TestActivities(unittest.TestCase):

    def setUp(self):
        self.asscns = associations()
        self.routines = routines(self.asscns)

    def test_routines(self):
        self.assertEqual(4, len(self.routines))
        self.assertIsInstance(self.routines[0], Clock)
        self.assertIsInstance(self.routines[1], Angel)
