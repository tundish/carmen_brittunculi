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
from carmen.logic import associations
from carmen.main import Game


class ClockTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_tick(self):
        clock = Clock(period=0.01, stop=3)
        session = Game.Session("uid", None, None, None, None)
        self.loop.run_until_complete(
            asyncio.wait(
                [clock(session, loop=self.loop)],
                loop=self.loop,
                timeout=12
            )
        )
        self.assertEqual(3, clock.turn)

class AngelTests(unittest.TestCase):

    def setUp(self):
        self.a = associations()

    def test_visit_closer(self):
        target = next(iter(self.a.search(label="Woodshed")))
        choice = next(iter(self.a.search(label="Kitchen")))
        options = (
            self.a.search(label="Kitchen") |
            self.a.search(label="Common house")
        )
        location = Angel.visit(self.a, target, options)
        self.assertIs(location, choice)

    def test_move_closer(self):
        actor = next(iter(self.a.search(_name="Civis Anatol Ant Bospor")))
        destn = next(iter(self.a.search(label="Marsh")))
        moves = list(Angel.moves(self.a, actor, destn))
        self.assertEqual(1, len(moves), moves)
