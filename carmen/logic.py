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

import datetime
from decimal import Decimal
from fractions import Fraction
import itertools
import logging
import pathlib
import random

import pkg_resources

from turberfield.dialogue.model import SceneScript

from carmen.agents import Clock
from carmen.agents import Angel
from carmen.orders import Orders
from carmen.routefinder import Routefinder
from carmen.types import Bowl
from carmen.types import Court
from carmen.types import CubbyFruit
from carmen.types import Dwelling
from carmen.types import Forest
from carmen.types import Heath
from carmen.types import Innkeeper
from carmen.types import Merchant
from carmen.types import Narrator
from carmen.types import Pit
from carmen.types import Player # noqa
from carmen.types import Priest
from carmen.types import Sanctum
from carmen.types import Settlement
from carmen.types import Spot
from carmen.types import Time
from carmen.types import Via
from carmen.types import Visibility
from carmen.types import Woodland
from carmen.types import Workings
from carmen.types import Woodsman

ides_of_march = datetime.date(396, 3, 1)

class Rules(Orders):

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    def __call__(
        self, folder, index, references, *,
        session, player=None, **kwargs
    ) -> dict:
        log = logging.getLogger(
            "{0!s}.{1}".format(session.uid, self.__class__.__name__)
        )
        player = player or next(i for i in references if isinstance(i, Player))
        metadata = {}
        keyword_args = self.kwargs.copy()
        keyword_args.update(kwargs)
        for n, name in self.sequence:
            method = getattr(self, name)
            rv = method(
                folder, index, references,
                session=session, player=player, log=log,
                **keyword_args
            )
            metadata.update(rv)
        return metadata

    @Orders.register()
    def day_night_cycle(
        self, folder, index, references, *,
        session, player, log, **kwargs
    ) -> dict:
        player.set_state(Time.advance(player.get_state(Time)))
        return folder.metadata

    @Orders.register()
    def windfall(
        self, folder, index, references, *,
        session, player, log,
        windfall_rate=None,
        **kwargs
    ) -> dict:
        windfall_rate = windfall_rate or Fraction(1, 4)

        items = [i for i in session.finder.lookup
                 if isinstance(i, (Bowl, CubbyFruit))]
        if any(
            i for i in items
            if i.get_state(Visibility) in (Visibility.new, Visibility.visible)
        ) or random.random() > windfall_rate:
            return folder.metadata

        if len(items) > 4:
            produce = [Bowl, CubbyFruit]
        else:
            produce = [CubbyFruit]

        cls = random.choice(produce)
        locns = [
            i for i in session.finder.lookup
            if cls in set(getattr(i, "produce", []))
        ]
        locn = random.choice(locns)
        obj = cls().set_state(locn.get_state(Spot)).set_state(Visibility.new)
        log.info(locn)
        log.info(obj)
        session.finder.register(None, obj)
        locn.set_state(Visibility.indicated)
        log.info("Created {0.__class__.__name__} at {1.label}.".format(obj, locn))
        return folder.metadata

    @Orders.register()
    def end_game(
        self, folder, index, references, *,
        session, player, log,
        windfall_rate=None,
        **kwargs
    ) -> dict:
        n_items = len(
            [i for i in session.finder.ensemble()
             if i.get_state(Visibility) == Visibility.hidden]
        )
        rv = folder.metadata.copy()
        if n_items > 6:
            rv["episode"] = 3
        return rv

def associations():
    rv = Routefinder()
    rv.register(
        Via.forwd,
        Woodland(label="Green lane").set_state(Spot.grid_1500),
        Settlement(label="South gate", produce=(CubbyFruit, )).set_state(Spot.grid_1302),
    )

    rv.register(
        Via.bidir,
        Settlement(label="Clearing", produce=(CubbyFruit, )).set_state(Spot.grid_1104),
        Woodland(label="Grove of Hades", produce=(Bowl, CubbyFruit)).set_state(Spot.grid_0804),
        Woodland(label="Stream", produce=(CubbyFruit, )).set_state(Spot.grid_0906),
        Dwelling(label="Woodshed").set_state(Spot.grid_1205),
        next(iter(rv.search(label="South gate"))),
    )

    rv.register(
        Via.bidir,
        Dwelling(label="Common house").set_state(Spot.grid_1208),
        Settlement(label="North gate", produce=(CubbyFruit, )).set_state(Spot.grid_1109),
        Dwelling(label="Kitchen").set_state(Spot.grid_1206),
    )
    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Kitchen"))),
        next(iter(rv.search(label="Woodshed"))),
    )
    rv.register(
        Via.bidir,
        Settlement(label="Footbridge", produce=(CubbyFruit, )).set_state(Spot.grid_0908),
        next(iter(rv.search(label="Stream"))),
        next(iter(rv.search(label="North gate"))),
    )

    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Grove of Hades"))),
        Heath(label="Quarry path", produce=(Bowl, )).set_state(Spot.grid_0610),
    )

    rv.register(
        Via.bckwd,
        Woodland(label="Rookery").set_state(Spot.grid_0913),
        Forest(label="Brambly dell").set_state(Spot.grid_0911),
        Forest(label="Copse").set_state(Spot.grid_0613),
        Forest(label="Woody tangle").set_state(Spot.grid_0816),
        Forest(label="Oak shrine").set_state(Spot.grid_1116),
        Forest(label="Prickly thicket").set_state(Spot.grid_1113),
    )

    rv.register(
        Via.forwd,
        next(iter(rv.search(label="Rookery"))),
        Forest(label="Shady lane").set_state(Spot.grid_1111),
    )

    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Woody tangle"))),
        next(iter(rv.search(label="Oak shrine"))),
    )

    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Oak shrine"))),
        next(iter(rv.search(label="Prickly thicket"))),
    )

    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Brambly dell"))),
        next(iter(rv.search(label="Shady lane"))),
        next(iter(rv.search(label="Copse"))),
    )

    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Shady lane"))),
        next(iter(rv.search(label="Prickly thicket"))),
        next(iter(rv.search(label="North gate"))),
        next(iter(rv.search(label="Brambly dell"))),
    )

    rv.register(
        Via.bidir,
        Heath(label="Scree").set_state(Spot.grid_1310),
        next(iter(rv.search(label="North gate"))),
        Heath(label="Ridge").set_state(Spot.grid_1413),
    )

    rv.register(
        Via.bckwd,
        next(iter(rv.search(label="Scree"))),
        Heath(label="Shelf").set_state(Spot.grid_0910),
    )
    rv.register(
        Via.forwd,
        next(iter(rv.search(label="Scree"))),
        Heath(label="Gully").set_state(Spot.grid_1610),
    )
    rv.register(
        Via.bidir,
        Workings(label="First hall", produce=(Bowl, )).set_state(Spot.grid_0211),
        Workings(label="South pit", produce=(Bowl, )).set_state(Spot.grid_0209),
        Pit(label="Quarry", produce=(Bowl, )).set_state(Spot.grid_0313),
    )
    rv.register(
        Via.bidir,
        Heath(label="Pulpit").set_state(Spot.grid_0318),
        Heath(label="Scramble").set_state(Spot.grid_0718),
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
        next(iter(rv.search(label="Quarry path"))),
        next(iter(rv.search(label="Shelf"))),
    )
    rv.register(
        Via.bidir,
        Heath(label="Sheep track").set_state(Spot.grid_1017),
        Heath(label="Cairn").set_state(Spot.grid_1416),
    )
    rv.register(
        Via.forwd,
        next(iter(rv.search(label="Oak shrine"))),
        next(iter(rv.search(label="Cairn"))),
    )
    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Cairn"))),
        next(iter(rv.search(label="Ridge"))),
        Woodland(label="Glade").set_state(Spot.grid_1717),
    )
    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Sheep track"))),
        next(iter(rv.search(label="Scramble"))),
    )
    rv.register(
        Via.bidir,
        Court(label="Mithraeum").set_state(Spot.grid_1614),
        Woodland(label="Pool").set_state(Spot.grid_1609),
        Sanctum(label="First chamber").set_state(Spot.grid_2114),
        next(iter(rv.search(label="Gully"))),
        next(iter(rv.search(label="Glade"))),
    )
    rv.register(
        Via.bidir,
        Sanctum(label="Second chamber").set_state(Spot.grid_2010),
        next(iter(rv.search(label="First chamber"))),
        Sanctum(label="Spelunca").set_state(Spot.grid_1807),
    )
    rv.register(
        Via.bidir,
        Sanctum(label="Hearth").set_state(Spot.grid_1605),
        next(iter(rv.search(label="Spelunca"))),
        Sanctum(label="Dormitory").set_state(Spot.grid_1603),
    )
    rv.register(
        Via.bidir,
        Sanctum(label="Armoury").set_state(Spot.grid_2005),
        next(iter(rv.search(label="Spelunca"))),
        Sanctum(label="Vault").set_state(Spot.grid_2003),
    )
    rv.register(
        Via.bidir,
        next(iter(rv.search(label="Pool"))),
        Woodland(label="Waterfall").set_state(Spot.grid_1508),
    )
    rv.register(
        Via.bidir,
        Heath(label="Marsh").set_state(Spot.grid_2117),
        next(iter(rv.search(label="Glade"))),
    )
    rv.register(
        None,
        Narrator()
    )

    rv.register(
        None,
        Merchant(name="Civis Anatol Ant Bospor").set_state(
            next(iter(rv.search(label="Common house"))).get_state(Spot)
        ),
    )

    rv.register(
        None,
        Woodsman(name="Derwodain Bryn Cariadoc").set_state(
            next(iter(rv.search(label="Quarry"))).get_state(Spot)
        ),
    )

    rv.register(
        None,
        Innkeeper(name="Maer Catrine Cadi Ingenbrettar").set_state(
            next(iter(rv.search(label="Kitchen"))).get_state(Spot)
        ),
    )

    rv.register(
        None,
        Priest(name="Offeiriad Dolphus Bifling").set_state(
            next(iter(rv.search(label="Mithraeum"))).get_state(Spot)
        ),
    )

    return rv

def routines(finder):
    return [
        Clock(period=15),
        Angel(
            next(iter(finder.search(_name="Civis Anatol Ant Bospor"))),
            (
                finder.search(label="Common house") |
                finder.search(label="Marsh")
            )
        ),
        Angel(
            next(iter(finder.search(_name="Derwodain Bryn Cariadoc"))),
            (
                finder.search(label="Common house") |
                finder.search(label="Quarry")
            )
        ),
        Angel(
            next(iter(finder.search(_name="Maer Catrine Cadi Ingenbrettar"))),
            (
                finder.search(label="Common house") |
                finder.search(label="Kitchen")
            )
        ),
    ]


episodes = [
    SceneScript.Folder(
        pkg="carmen",
        description="Dialogue for a game episode 1.",
        metadata={"episode": Decimal(1)},
        paths=sorted([
            str(i.relative_to(
                pkg_resources.resource_filename("carmen", "")
            ))
            for i in pathlib.Path(
                pkg_resources.resource_filename("carmen", "dialogue/ep_01")
            ).glob("*/*.rst")
        ]),
        interludes=itertools.repeat(Rules())
    ),
    SceneScript.Folder(
        pkg="carmen",
        description="Dialogue for game episode 2.",
        metadata={"episode": Decimal(2)},
        paths=sorted([
            str(i.relative_to(
                pkg_resources.resource_filename("carmen", "")
            ))
            for i in pathlib.Path(
                pkg_resources.resource_filename("carmen", "dialogue/ep_02")
            ).glob("*/*.rst")
        ]),
        interludes=itertools.repeat(Rules(windfall_rate=1))
    ),
    SceneScript.Folder(
        pkg="carmen",
        description="Game over.",
        metadata={"episode": Decimal(3)},
        paths=sorted([
            str(i.relative_to(
                pkg_resources.resource_filename("carmen", "")
            ))
            for i in pathlib.Path(
                pkg_resources.resource_filename("carmen", "dialogue/exit")
            ).glob("*.rst")
        ]),
        interludes=itertools.repeat(None)
    )
]

first, *rest = episodes

rehearsal = list(associations().ensemble()) + [
    Player(name="Player").set_state(Spot.grid_1205).set_state(Time.eve_predawn)
]
