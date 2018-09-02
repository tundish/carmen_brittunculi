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

from collections import namedtuple
import logging
import re

from turberfield.dialogue.model import Model

# TODO: Inherit from Performer?
# TODO: Unify with Quest?
class Handler:

    validation = {
        "email": re.compile(
            "[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]"
            "+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9]"
            "(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+"
            # http://www.w3.org/TR/html5/forms.html#valid-e-mail-address
        ),
        "location": re.compile("[0-9a-f]{32}"),
        "name": re.compile("[A-Z a-z]{2,32}"),
        "quest": re.compile("[0-9a-f]{32}"),
    }

    Element = namedtuple("Element", ["dialogue", "shot", "offset", "duration"])

    @staticmethod
    def frames(seq, dwell, pause):
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
                    frame.append(Handler.Element(item, shot, item.offset, item.duration))

            elif isinstance(item, Model.Line):
                durn = pause + dwell * item.text.count(" ")
                frame.append(Handler.Element(item, shot, offset, durn))
                offset += durn
            else:
                frame.append(Handler.Element(item, shot, offset, offset))
        else:
            yield frame

    @staticmethod
    def react(quest, frame, loop=None):
        log = logging.getLogger(str(quest.uid))
        for element in frame:
            event = element.dialogue
            if isinstance(event, Model.Property) and event.object is not None:
                setattr(event.object, event.attr, event.val)
                log.info("React on property {0}".format(event))
                yield event

