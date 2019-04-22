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

import itertools
import unittest

import carmen.logic
from carmen.types import Location

class RoutefinderTests(unittest.TestCase):

    def setUp(self):
        self.associations = carmen.logic.associations()

    def test_navigation(self):
        locns = [i for i in self.associations.ensemble() if isinstance(i, Location)]
        for locn, dest in itertools.permutations(locns, r=2):
            if dest.label != "Green lane":
                with self.subTest(locn=locn, dest=dest):
                    route = self.associations.route(locn, dest, maxlen=3*len(locns))
                    self.assertTrue(route, route)
