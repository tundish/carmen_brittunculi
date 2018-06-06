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

# TODO:: Remove all this code

from collections import namedtuple
import random

class Scenery:

    Leaf = namedtuple("Leaf", ["ref", "x", "y"])

    @staticmethod
    def forest(
        width, height,
        population=[
            "svg-leaf-00",
            "svg-leaf-01",
            "svg-leaf-01",
            "svg-leaf-01",
            "svg-leaf-01",
            "svg-leaf-01",
            "svg-leaf-01",
            "svg-leaf-02"
        ],
        pitch=(24, 24)
    ):
        """
            TODO: Switch to better techniques, eg:

            http://devmag.org.za/2009/05/03/poisson-disk-sampling/
            https://codepen.io/alvov/pen/vgLevP (SVG lighting shader).
            https://css-tricks.com/look-svg-light-source-filters/

            Generate scenes in offline batches and select by eye.

        """
        choice = random.choice
        randint = random.randint
        pitch_x, pitch_y = pitch
        return [
            Scenery.Leaf(choice(population), x + randint(0, pitch_x), y + randint(0, pitch_y))
            for x in range(0, width, pitch_x)
            for y in range(0, height, pitch_y)
        ]


