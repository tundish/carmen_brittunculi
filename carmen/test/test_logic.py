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

import unittest

from carmen.logic import associations
from carmen.main import World
from carmen.types import Location
from carmen.types import Via

class TestNavigation(unittest.TestCase):

    def setUp(self):
        self.a = associations()
        import pprint
        pprint.pprint(self.a.lookup)

    def test_new_world(self):
        uid = World.quest("Stig")
        assoc = World.quests[uid]
        rv = assoc.search(label="North gate")
        self.assertEqual(1, len(rv))

    def test_associations(self):
        locn = next(iter(self.a.search(label="Grove of Hades")))
        neighbours = self.a.match(
            locn,
            forward=[Via.bidir, Via.forwd],
            reverse=[Via.bidir, Via.bckwd],
            predicate=lambda x: isinstance(x, Location)
        )
        self.assertEqual(4, len(neighbours))
