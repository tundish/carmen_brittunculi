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

from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.types import Player

from carmen.frame import Frame

class FrameTests(unittest.TestCase):

    @staticmethod
    def dialogue(model):
        """ Fakes Turberfield dialogue performer."""
        for shot, item in model:
            yield shot
            yield item

    def setUp(self):
        self.ensemble = [
            Player(name="QA")
        ]

    def test_frame_from_dialogue(self):
        content = textwrap.dedent("""
            .. entity:: P

            Scene
            ~~~~~

            Shot
            ----

            [P]_

                |P_FIRSTNAME| says, "{0}".

            .. |P_FIRSTNAME| property:: P.name.firstname
            """.format("Hello"))
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select(self.ensemble))
        rv = list(Frame.items(FrameTests.dialogue(script.run()), dwell=0.3, pause=1))
        self.assertEqual(1, len(rv))

    def test_single_fx_in_frame(self):
        content = textwrap.dedent("""
            .. entity:: P

            Scene
            ~~~~~

            Shot
            ----

            [P]_

                |P_FIRSTNAME| says, "{0}".

            .. fx:: logic slapwhack.wav
               :offset: 0
               :duration: 3000
               :loop: 1

            [P]_

                |P_FIRSTNAME| says, "{0}".

            .. |P_FIRSTNAME| property:: P.name.firstname
            """.format("Hello"))
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select(self.ensemble))
        rv = list(Frame.items(FrameTests.dialogue(script.run()), dwell=0.3, pause=1))
        self.assertEqual(1, len(rv))

    def test_second_shot_splits_frame(self):
        content = textwrap.dedent("""
            .. entity:: P

            Scene
            ~~~~~

            One
            ---

            [P]_

                |P_FIRSTNAME| says, "{0}".

            .. fx:: logic slapwhack.wav
               :offset: 0
               :duration: 3000
               :loop: 1

            [P]_

                |P_FIRSTNAME| says, "{0}".

            Two
            ---

            [P]_

                |P_FIRSTNAME| says, "{0}".

            .. |P_FIRSTNAME| property:: P.name.firstname
            """.format("Hello"))
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select(self.ensemble))
        rv = list(Frame.items(FrameTests.dialogue(script.run()), dwell=0.3, pause=1))
        self.assertEqual(2, len(rv))

    def test_second_fx_splits_frame(self):
        content = textwrap.dedent("""
            .. entity:: P

            Scene
            ~~~~~

            Shot
            ----

            [P]_

                |P_FIRSTNAME| says, "{0}".

            .. fx:: logic slapwhack.wav
               :offset: 0
               :duration: 3000
               :loop: 1

            [P]_

                |P_FIRSTNAME| says, "{0}".

            .. fx:: logic slapwhack.wav
               :offset: 0
               :duration: 3000
               :loop: 1

            [P]_

                |P_FIRSTNAME| says, "{0}".

            .. |P_FIRSTNAME| property:: P.name.firstname
            """.format("Hello"))
        script = SceneScript("inline", doc=SceneScript.read(content))
        script.cast(script.select(self.ensemble))
        rv = list(Frame.items(FrameTests.dialogue(script.run()), dwell=0.3, pause=1))
        self.assertEqual(2, len(rv))
