#!/usr/bin/env python3
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

__doc__ = """
Example:

python3 scenery.py --symbol leaf > scenery.svg


"""
import argparse
import cmath
from collections import defaultdict
from collections import deque
import itertools
import random
import sys

# TODO: convert symbol -> defs but without own attributes
# TODO: add title, desc
svg = """
<svg xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="{width}" height="{height}"
viewBox="0 0 {width} {height}"
preserveAspectRatio="none"
>
{0}
</svg>
"""

use = """
<use class="{klass}"
x="{point.real:.0f}" y="{point.imag:.0f}" transform="inherit"
xlink:href="#{name}" />
"""

style = """
<style type="text/css">
#use.med {transform: scale(1.4);}
#use.r45 {transform: rotate(45 16 16);}
</style>
"""

symbols = {
"spot": (5, """
<symbol id="spot">
<circle stroke="red" fill="dimgrey" stroke-width="1"
cx="3" cy="3" r="2"
/>
</symbol>"""),
"leaf": (16, """
<symbol id="leaf">
<path
    d="M 12 11 C 21,2 17,22 23,27 C 8,25 3,11 12,11 z M 18,16 C 16,14 17,22 20,24 z"
    stroke-width="0.2"
    stroke="yellow"
    fill="green"
    fill-rule="evenodd"
    transform="inherit"
/>
</symbol>"""),
}

DEFAULT_WIDTH = 360
DEFAULT_HEIGHT = 600
DEFAULT_POINTS = 600
DEFAULT_SYMBOL = "spot"


def overlaps(this, that, span):
    return cmath.isclose(this, that, abs_tol=span)

def sow(seed, min_dist, max_dist):
    r = random.uniform(min_dist, max_dist)
    phi = random.uniform(0, 2 * cmath.pi)
    return seed + cmath.rect(r, phi)

def poisson_disk(
    n_points, gaps, seeds,
    n_gen=12, min_dist=16, max_dist=42,
    origin=complex(0, 0), top=complex(DEFAULT_WIDTH, DEFAULT_HEIGHT)
):
    q = deque(seeds)
    pop = set(seeds)
    while len(pop) < n_points:
        try:
            s = q.popleft()
        except IndexError:
            return

        gap = random.choice(gaps)
        for p in (sow(s, min_dist, max_dist) for i in range(n_gen)):
            if (
                not any(overlaps(i, p, gap) for i in pop) and
                origin.real <= p.real < top.real - gap and
                origin.imag <= p.imag < top.imag - gap
            ):
                q.append(p)
                pop.add(p)
                yield p, gap

def paint(points, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    content = [style]
    content.extend([s.strip() for n, s in symbols.values()])
    content.extend([
        use.format(klass=" ".join(classes), name=name, point=point).strip()
        for classes, name, point in points
    ])
    return svg.format("\n".join(content), width=width, height=height)

def parser(description=__doc__):
    rv = argparse.ArgumentParser(
        description,
        fromfile_prefix_chars="@"
    )
    rv.add_argument(
        "--spacing", action="append", type=float,
        help="Give a sequence of pixel sizes for spacing."
    )
    rv.add_argument(
        "--symbol", action="append", type=str, default=[],
        help="Pick one or more symbol to use ({0}) [{1}].".format(
            ",".join(symbols.keys()), DEFAULT_SYMBOL
        )
    )
    rv.add_argument(
        "--debug", action="store_true", default=False,
        help="Print extra info (slow)."
    )
    rv.add_argument(
        "--points", type=int, default=DEFAULT_POINTS,
        help="The number of generated points [{0}].".format(DEFAULT_POINTS)
    )
    rv.add_argument(
        "--width", type=int, default=DEFAULT_WIDTH,
        help="The width in pixels [{0}].".format(DEFAULT_WIDTH)
    )
    rv.add_argument(
        "--height", type=int, default=DEFAULT_HEIGHT,
        help="The height in pixels [{0}].".format(DEFAULT_HEIGHT)
    )
    return rv

def main(args):
    scene = []
    names = args.symbol or [DEFAULT_SYMBOL]
    spacing = [symbols[name][0] for name in names]
    lookup = defaultdict(list)
    for name in names:
        gap, data = symbols[name]
        lookup[gap].append(name)

    classes = ["plain", "r45", "med"]
    pad = max(symbols[name][0] for name in args.symbol)
    height = args.height - pad
    width = args.width - pad
    for n, (point, gap) in enumerate(
        poisson_disk(
            args.points,
            spacing,
            seeds=[
                complex(width / 3, height / 3),
                complex(2 * width / 3, height / 3),
                complex(2 * width / 3, 2 * height / 3)
            ],
            top=complex(width, height)
        )
    ):
        name = random.choice(lookup[gap])
        scene.append((
            random.choice(list(itertools.combinations(
                classes, random.randint(1, len(classes))
            ))),
            name,
            point
        ))
        if args.debug:
            print(name, gap, point, file=sys.stderr)

    print("{0} items".format(n), file=sys.stderr)
    print(paint(scene, args.width + pad, args.height + pad), file=sys.stdout)
    return 0

def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
