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

from decimal import Decimal
import unittest

from carmen.types import Compass
from carmen.types import Spot
from carmen.types import Time
from turberfield.utils.assembly import Assembly

class TimeTests(unittest.TestCase):

    def test_time_sequence_from_superstate(self):
        then = Time.eve
        now = Time.advance(then)
        self.assertEqual(Time.eve_evening, now)

    def test_time_sequence_past_superstate(self):
        then = Time.day_dusk
        now = Time.advance(then)
        self.assertEqual(Time.eve_sunset, now)

class CompassTests(unittest.TestCase):

    def test_bearing_from_complex(self):
        self.assertEqual(Decimal(360), Compass.bearing(complex(0, 1)))
        self.assertEqual(Decimal(45), Compass.bearing(complex(1, 1)))
        self.assertEqual(Decimal(90), Compass.bearing(complex(1, 0)))
        self.assertEqual(Decimal(135), Compass.bearing(complex(1, -1)))
        self.assertEqual(Decimal(180), Compass.bearing(complex(0, -1)))
        self.assertEqual(Decimal(225), Compass.bearing(complex(-1, -1)))
        self.assertEqual(Decimal(270), Compass.bearing(complex(-1, 0)))
        self.assertEqual(Decimal(315), Compass.bearing(complex(-1, 1)))

    def test_legend_from_degrees(self):
        self.assertEqual("North", Compass.legend(0))
        self.assertEqual("South", Compass.legend(180))
        self.assertEqual("East", Compass.legend(90))
        self.assertEqual("West", Compass.legend(270))
        self.assertEqual("NorthWest", Compass.legend(Decimal("292.6")))
        self.assertEqual("NorthWest", Compass.legend(315))
        self.assertEqual("NorthWest", Compass.legend(Decimal("337.5")))
        self.assertEqual("North", Compass.legend(Decimal("337.6")))
        self.assertEqual("North", Compass.legend(360))

    def test_legend_from_complex(self):
        self.assertEqual("North", Compass.legend(complex(0, 1)))
        self.assertEqual("NorthEast", Compass.legend(complex(1, 1)))
        self.assertEqual("East", Compass.legend(complex(1, 0)))
        self.assertEqual("SouthEast", Compass.legend(complex(1, -1)))
        self.assertEqual("South", Compass.legend(complex(0, -1)))
        self.assertEqual("SouthWest", Compass.legend(complex(-1, -1)))
        self.assertEqual("West", Compass.legend(complex(-1, 0)))
        self.assertEqual("NorthWest", Compass.legend(complex(-1, 1)))

class SpotTests(unittest.TestCase):

    def test_assemble_spot(self):
        obj = list(Spot)[0]
        data = Assembly.dumps(obj)
        self.assertTrue(data)
        rv = Assembly.loads(data)
        self.assertIsInstance(rv, Spot)
        self.assertEqual(obj.value, rv.value)
