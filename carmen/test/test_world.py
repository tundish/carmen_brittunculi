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

import textwrap
import unittest

import carmen.logic
from carmen.main import World
from carmen.types import Location
from carmen.types import Spot
from carmen.utils import Scenery

class WorldTests(unittest.TestCase):

    tmplt = textwrap.dedent(
        """
        ..  This is a Turberfield dialogue file (reStructuredText).
            Scene ~~
            Shot --

        .. |VERSION| property:: carmen.logic.version

        :author: D Haynes
        :date: 2018-04-11
        :project: carmen
        :version: |VERSION|

        .. entity:: LOCATION
           :types: carmen.logic.Location
           :states: carmen.logic.Spot.{spot}

        .. entity:: PLAYER
           :types: carmen.logic.Player
           :states: carmen.logic.Spot.{spot}

        {label}
        {title}

        Looking around
        --------------

        [LOCATION]_

            It's Green.
        """
    )

    @unittest.skip("utility function")
    def test_gen_dialogue_script_files(self):
        asscns = carmen.logic.associations()
        locns = [i for i in asscns.ensemble() if isinstance(i, Location)]

        for locn in locns:
            name = locn.label.lower().replace(" ", "_")
            with open(name + ".rst", "w") as out:
                out.write(WorldTests.tmplt.format(
                    label=locn.label, title="~" * len(locn.label),
                    spot=locn.get_state(Spot).name
                ))

    def test_forest(self):
        leaves = Scenery.forest(64, 64)
        self.assertTrue(5 <= len(leaves) <= 12, leaves)
