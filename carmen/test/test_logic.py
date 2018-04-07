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

class TestNavigation(unittest.TestCase):

    def setUp(self):
        self.a = associations()

    def test_new_world(self):
        uid = World.quest("Stig")
        self.fail(World.quests[uid])

    def test_associations(self):
        rv = self.a.search(label="Grove of Hades")
        self.fail(rv)
