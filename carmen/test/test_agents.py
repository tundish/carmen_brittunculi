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


class ClockTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_tick(self):
        #test = self.loop.create_task(
        #    run_then_cancel(coro, progress, down, up, loop=loop)
        #)
        clock = Clock(stop=3)
        #test = self.loop.create_task(clock(loop=self.loop))
        self.loop.run_until_complete(clock(loop=self.loop))
        self.fail(clock)
