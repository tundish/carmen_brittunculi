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

from collections import deque
import datetime
from fractions import Fraction
import itertools
import logging
import pathlib
import random

import pkg_resources

from turberfield.dialogue.model import SceneScript

from carmen import __version__ as version # noqa
from carmen.agents import Affinity
from carmen.agents import Clock
from carmen.agents import Motivator
from carmen.orders import Orders
from carmen.routefinder import Routefinder
from carmen.types import Character
from carmen.types import CubbyFruit
from carmen.types import Location
from carmen.types import Narrator
from carmen.types import Player # noqa
from carmen.types import Spot
from carmen.types import Time
from carmen.types import Via
from carmen.types import Visibility
from carmen.types import Wants

ides_of_march = datetime.date(396, 3, 1)

class Rules(Orders):

    zone = [
        i for i in Spot
        if i.value and
        8 <= i.value.real <= 15 and
        0 <= i.value.imag <= 9
    ]

    def __init__(self, windfall_rate=None):
        super().__init__()
        self.windfall_rate = windfall_rate or Fraction(1, 4)

    def __call__(
        self, folder, index, references, *,
        session, player=None, **kwargs
    ) -> dict:
        log = logging.getLogger(
            "{0!s}.{1}".format(session.uid, self.__class__.__name__)
        )
        player = player or next(i for i in references if isinstance(i, Player))
        metadata = {}
        for n, name in self.sequence:
            method = getattr(self, name)
            rv = method(
                folder, index, references,
                session=session, player=player, log=log,
                **kwargs
            )
            metadata.update(rv)
        return metadata

    @Orders.register()
    def day_night_cycle(
        self, folder, index, references, *,
        session, player, log, **kwargs
    ) -> dict:
        player.set_state(Time.advance(player.get_state(Time)))

        if player.get_state(Time) == Time.day_dinner:
            player.set_state(Wants.needs_food)
        elif player.get_state(Time) == Time.eve_midnight:
            player.set_state(Wants.needs_sleep)
        elif player.get_state(Time) == Time.day_sunrise:
            player.set_state(Wants.nothing)

        return folder.metadata

    @Orders.register()
    def windfall(
        self, folder, index, references, *,
        session, player, log, **kwargs
    ) -> dict:

        if any(
            i for i in session.finder.lookup
            if isinstance(i, CubbyFruit) and
            i.get_state(Visibility) in (Visibility.new, Visibility.visible)
        ) or random.random() > self.windfall_rate:
            return folder.metadata

        locns = [
            i for i in session.finder.lookup
            if getattr(i, "label", None) in (
                "South gate", "Clearing", "Grove of Hades",
                "Stream", "Footbridge", "North gate"
            )
        ]
        locn = random.choice(locns)
        obj = CubbyFruit().set_state(locn.get_state(Spot)).set_state(Visibility.new)
        session.finder.register(None, obj)
        locn.set_state(Visibility.indicated)
        log.info("Created {0.__class__.__name__} at {1.label}.".format(obj, locn))
        return folder.metadata

def associations():
    rv = Routefinder()
    rv.register(
        Via.forwd,
        Location(label="Green lane").set_state(Spot.grid_1500),
        Location(label="South gate").set_state(Spot.grid_1302),
    )

    rv.register(
        Via.bidir,
        Location(label="Clearing").set_state(Spot.grid_1104),
        Location(label="Grove of Hades").set_state(Spot.grid_0804),
        Location(label="Stream").set_state(Spot.grid_0906),
        Location(label="North gate").set_state(Spot.grid_1109),
        Location(label="Common house").set_state(Spot.grid_1306),
        next(iter(rv.search(label="South gate"))),
    )

    rv.register(
        Via.bidir,
        Location(label="Footbridge").set_state(Spot.grid_0908),
        next(iter(rv.search(label="Stream"))),
        next(iter(rv.search(label="North gate"))),
    )

    rv.register(
        Via.bidir,
        Location(label="Kitchen").set_state(Spot.grid_1308),
        next(iter(rv.search(label="Common house"))),
        Location(label="Woodshed").set_state(Spot.grid_1407),
    )
    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Grove of Hades"))),
        Location(label="Quarry path").set_state(Spot.grid_0610),
    )

    rv.register(
        Via.bidir,
        Location(label="Rookery").set_state(Spot.grid_1113),
        Location(label="Shady lane").set_state(Spot.grid_0909),
        Location(label="Copse").set_state(Spot.grid_0813),
        Location(label="Woody tangle").set_state(Spot.grid_0816),
        Location(label="Brambly dell").set_state(Spot.grid_1116),
        Location(label="Oak shrine").set_state(Spot.grid_1416),
        Location(label="Prickly thicket").set_state(Spot.grid_1413),
    )

    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Oak shrine"))),
        next(iter(rv.search(label="Brambly dell"))),
        next(iter(rv.search(label="Prickly thicket"))),
    )

    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Woody tangle"))),
        next(iter(rv.search(label="Copse"))),
        next(iter(rv.search(label="Brambly dell"))),
    )

    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Shady lane"))),
        next(iter(rv.search(label="North gate"))),
        next(iter(rv.search(label="Copse"))),
    )

    rv.register(
        Via.bidir,
        Location(label="Scree").set_state(Spot.grid_1111),
        next(iter(rv.search(label="North gate"))),
        Location(label="Ridge").set_state(Spot.grid_1113),
    )

    rv.register(
        Via.bckwd,
        next(iter(rv.search(label="Scree"))),
        Location(label="Shelf").set_state(Spot.grid_0911),
    )
    rv.register(
        Via.forwd,
        next(iter(rv.search(label="Scree"))),
        Location(label="Gully").set_state(Spot.grid_1411),
    )
    rv.register(
        Via.bidir,
        Location(label="First hall").set_state(Spot.grid_0214),
        Location(label="South pit").set_state(Spot.grid_0211),
        Location(label="Quarry").set_state(Spot.grid_0714),
    )
    rv.register(
        Via.bidir,
        Location(label="Pulpit").set_state(Spot.grid_0318),
        Location(label="Scramble").set_state(Spot.grid_0718),
    )
    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Quarry path"))),
        next(iter(rv.search(label="Quarry"))),
    )
    rv.register(
        Via.forwd,
        next(iter(rv.search(label="Scramble"))),
        next(iter(rv.search(label="Quarry"))),
    )
    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Quarry"))),
        next(iter(rv.search(label="Shelf"))),
    )
    rv.register(
        Via.bidir,
        Location(label="Sheep track").set_state(Spot.grid_1017),
        Location(label="Cairn").set_state(Spot.grid_1115),
    )
    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Cairn"))),
        next(iter(rv.search(label="Ridge"))),
    )
    rv.register(
        Via.forwd,
        next(iter(rv.search(label="Sheep track"))),
        next(iter(rv.search(label="Scramble"))),
    )
    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Cairn"))),
        next(iter(rv.search(label="Copse"))),
    )
    rv.register(
        Via.bidir,
        Location(label="Mithraeum").set_state(Spot.grid_1614),
        next(iter(rv.search(label="Gully"))),
        Location(label="Pool").set_state(Spot.grid_1610),
        Location(label="First chamber").set_state(Spot.grid_2114),
    )
    rv.register(
        Via.bidir,
        Location(label="Second chamber").set_state(Spot.grid_2010),
        next(iter(rv.search(label="First chamber"))),
        Location(label="Spelunca").set_state(Spot.grid_1807),
    )
    rv.register(
        Via.bidir,
        Location(label="Hearth").set_state(Spot.grid_1605),
        next(iter(rv.search(label="Spelunca"))),
        Location(label="Dormitory").set_state(Spot.grid_1603),
    )
    rv.register(
        Via.bidir,
        Location(label="Armoury").set_state(Spot.grid_2005),
        next(iter(rv.search(label="Spelunca"))),
        Location(label="Vault").set_state(Spot.grid_2003),
    )
    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Pool"))),
        Location(label="Waterfall").set_state(Spot.grid_1508),
    )
    rv.register(
        Via.bidir,
        Location(label="Marsh").set_state(Spot.grid_2117),
        Location(label="Glade").set_state(Spot.grid_1717),
    )
    rv.register(
        Via.forwd,
        next(iter(rv.search(label="Mithraeum"))),
        next(iter(rv.search(label="Glade"))),
    )
    rv.register(
        Via.forwd,
        next(iter(rv.search(label="Glade"))),
        next(iter(rv.search(label="Copse"))),
    )
    rv.register(
        None,
        Narrator()
    )

    rv.register(
        None,
        Character(name="Civis Anatol Ant Bospor").set_state(
            next(iter(rv.search(label="Common house"))).get_state(Spot)
        ),
    )

    rv.register(
        None,
        Character(name="Maer Catrine Cadi Ingenbrettar").set_state(
            next(iter(rv.search(label="Kitchen"))).get_state(Spot)
        ),
    )

    return rv

def activities(finder):
    return [
        Clock(),
        # Creator(finder, CubbyFruit, probability=Fraction(1, 8)),
        Motivator(
            next(iter(finder.search(_name="Civis Anatol Ant Bospor"))),
            finder,
            Affinity(
                finder.search(label="Common house") |
                finder.search(label="Marsh"),
                deque([])
            )
        )
    ]


episodes = [
    SceneScript.Folder(
        pkg="carmen",
        description="Dialogue for a Game Episode 1.",
        metadata={},
        paths=[
            str(i.relative_to(
                pkg_resources.resource_filename("carmen", "")
            ))
            for i in pathlib.Path(
                pkg_resources.resource_filename("carmen", "dialogue/ep_01")
            ).glob("*.rst")
        ],
        interludes=itertools.repeat(Rules(windfall_rate=1))
    ),
    SceneScript.Folder(
        pkg="carmen",
        description="Location descriptions.",
        metadata={},
        paths=[
            str(i.relative_to(
                pkg_resources.resource_filename("carmen", "")
            ))
            for i in pathlib.Path(
                pkg_resources.resource_filename("carmen", "dialogue/local")
            ).glob("*.rst")
        ],
        interludes=itertools.repeat(Rules())
    )
]

first, *rest = episodes

rehearsal = list(associations().ensemble()) + [
    Player(name="Player").set_state(Spot.grid_1407).set_state(Time.eve_predawn)
]
