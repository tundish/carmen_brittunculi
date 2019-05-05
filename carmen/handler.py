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
import itertools
import logging
import pathlib
import random
import re

import pkg_resources

from turberfield.dialogue.model import Model

from carmen.types import Dwelling
from carmen.types import Forest
from carmen.types import Heath
from carmen.types import Pit
from carmen.types import Sanctum
from carmen.types import Woodland
from carmen.types import Workings


class Handler:

    validation = {
        "email": re.compile(
            "[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]"
            "+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9]"
            "(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+"
            # http://www.w3.org/TR/html5/forms.html#valid-e-mail-address
        ),
        "location": re.compile("[0-9a-f]{32}"),
        "name": re.compile("[A-Z a-z]{2,42}"),
        "session": re.compile("[0-9a-f]{32}"),
    }

    Element = namedtuple("Element", ["source", "dialogue", "shot", "offset", "duration"])

    @staticmethod
    def frames(source, seq, dwell, pause):
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
                    frame.append(Handler.Element(
                        source, item, shot, item.offset / 1000, item.duration / 1000
                    ))

            elif isinstance(item, Model.Line):
                durn = pause + dwell * item.text.count(" ")
                frame.append(Handler.Element(source, item, shot, offset, durn))
                offset += durn
            elif not isinstance(item, Model.Condition):
                frame.append(Handler.Element(source, item, shot, offset, 0))
        else:
            if any(isinstance(i.dialogue, (Model.Audio, Model.Line)) for i in frame):
                yield frame

    @staticmethod
    def react(session, frame, loop=None):
        log = logging.getLogger(str(session.uid))
        metadata = session.cache.get("metadata", {})
        for element in frame:
            event = element.dialogue
            if isinstance(event, Model.Property) and event.object is not None:
                setattr(event.object, event.attr, event.val)
                log.debug("React on property {0}".format(event))
            elif callable(event):
                metadata.update(event(session=session, loop=loop))
                log.debug("React on interlude {0}".format(event))
            yield element

    @staticmethod
    def refresh(frame, min_val=8):
        try:
            return max(
                [min_val] +
                [i.offset + i.duration for i in frame if i.duration]
            )
        except ValueError:
            return None

    @staticmethod
    def scenery(location):
        root = pkg_resources.resource_filename("carmen", "static")
        parent = pkg_resources.resource_filename("carmen", "static/svg")
        if isinstance(location, (Forest, Heath, Woodland)):
            pattern = "scenery-leaf*.svg"
        elif isinstance(location, Dwelling):
            pattern = "scenery-wattle*.svg"
        elif isinstance(location, (Pit, Workings)):
            pattern = "scenery-rock*.svg"
        elif isinstance(location, Sanctum):
            pattern = "scenery-slab*.svg"
        else:
            pattern = "scenery-none.svg"
        assets = [
            i.relative_to(root) for i in pathlib.Path(parent).glob(pattern)
        ]
        random.shuffle(assets)
        return itertools.cycle(assets or ["hack_throws_404.svg"])
