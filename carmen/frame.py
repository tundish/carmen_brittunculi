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


from turberfield.dialogue.model import Model

class Frame:

    @staticmethod
    def items(seq, dwell, pause):
        """
        A new Frame on each Shot, and every FX item.

        """
        shot = None
        frame = []
        offset = 0
        for item in seq:
            if isinstance(item, (Model.Audio, Model.Shot)):
                if frame and shot and shot != item:
                    yield frame
                    frame = []
                    offset = 0

                if isinstance(item, Model.Shot):
                    shot = item
                else:
                    frame.append((item.duration, item.offset, item))

            elif isinstance(item, Model.Line):
                durn = pause + dwell * item.text.count(" ")
                frame.append((durn, offset, item))
                offset += durn
        else:
            yield frame
