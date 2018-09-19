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

from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.performer import Performer

from carmen.handler import Handler
from carmen.types import Narrator
from carmen.types import Player
from carmen.types import Wants

class HandlerTests(unittest.TestCase):

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
        rv = list(Handler.frames(HandlerTests.dialogue(script.run()), dwell=0.3, pause=1))
        self.assertEqual(1, len(rv))

    def test_single_fx_splits_frame(self):
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
        rv = list(Handler.frames(HandlerTests.dialogue(script.run()), dwell=0.3, pause=1))
        self.assertEqual(2, len(rv))
        self.assertTrue(all(i for i in rv))
        self.assertIsInstance(rv[1][0].dialogue, Model.Audio)

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
        rv = list(Handler.frames(HandlerTests.dialogue(script.run()), dwell=0.3, pause=1))
        self.assertEqual(3, len(rv))
        self.assertTrue(all(i for i in rv))
        self.assertIsInstance(rv[1][0].dialogue, Model.Audio)

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
        rv = list(Handler.frames(HandlerTests.dialogue(script.run()), dwell=0.3, pause=1))
        self.assertEqual(3, len(rv), rv)
        self.assertTrue(all(i for i in rv))
        self.assertIsInstance(rv[1][0].dialogue, Model.Audio)
        self.assertIsInstance(rv[2][0].dialogue, Model.Audio)

    def test_handler_frames_conditional_dialogue(self):
        content = textwrap.dedent("""

        .. entity:: PLAYER
           :types: carmen.logic.Player
           :states: carmen.types.Wants.needs

        .. entity:: NARRATOR
           :types: carmen.logic.Narrator

        Wants
        ~~~~~

        Hungry
        ------

        .. condition:: PLAYER.state carmen.types.Wants.needs_food

        [NARRATOR]_

            You're hungry.

        [NARRATOR]_

            Nom nom nom.

        Tired
        -----

        .. condition:: PLAYER.state carmen.types.Wants.needs_sleep

        [NARRATOR]_

            You're tired.


        [NARRATOR]_

            ZZZZZZZZ.

            """)
        script = SceneScript("inline", doc=SceneScript.read(content))
        ensemble = [Player(name="test").set_state(Wants.needs_food), Narrator()]
        script.cast(script.select(ensemble))
        rv = list(Handler.frames(
            HandlerTests.dialogue(script.run()), dwell=0.3, pause=1
        ))
        self.assertEqual(2, len(rv), rv)
        self.assertIsInstance(rv[0][0].dialogue, Model.Condition)
        self.assertTrue(Performer.allows(rv[0][0].dialogue))
        self.assertIsInstance(rv[0][1].dialogue, Model.Line)
        self.assertEqual(0, rv[0][1].offset)
        self.assertEqual(1.3, rv[0][1].duration)
        self.assertEqual(1.3, rv[0][2].offset)
        self.assertEqual(1.6, rv[0][2].duration)
        self.assertAlmostEqual(2.9, Handler.refresh(rv[0]))

        self.assertIsInstance(rv[1][0].dialogue, Model.Condition)
        self.assertFalse(Performer.allows(rv[1][0].dialogue))
        self.assertIsInstance(rv[1][1].dialogue, Model.Line)
        self.assertEqual(0, rv[1][1].offset)
        self.assertEqual(1.3, rv[1][1].duration)
        self.assertEqual(1.3, rv[1][2].offset)
        self.assertEqual(1.0, rv[1][2].duration)
        self.assertAlmostEqual(2.3, Handler.refresh(rv[1]))

