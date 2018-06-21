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

__doc__ = """
Example:

python3 disk_sample.py --spacing 24 --spacing 24 --spacing 32 > carmen/static/svg/poisson.svg

"""
import argparse
import cmath
from collections import deque
import random
import sys

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
x="{point.real:.0f}" y="{point.imag:.0f}"
xlink:href="#{name}" />
"""

symbols = {
    5: [
        ("spot", """
<symbol id="spot">
<circle stroke="red" fill="dimgrey" stroke-width="1"
cx="3" cy="3" r="2"
/>
</symbol>
                """),
    ],
    24: [
        ("svg-leaf-00", """
<symbol id="svg-leaf-00">
<path
    d="M 12 11 C 21,2 17,22 23,27 C 8,25 3,11 12,11 z M 18,16 C 16,14 17,22 20,24 z"
    stroke-width="0.2"
    stroke="yellow"
    fill="currentColor"
    fill-rule="evenodd"
/>
</symbol>
                """),
    ],
    32: [
        ("svg-leaf-01", """
<symbol id="svg-leaf-01">
<path
    d="M 12 11 C 21,2 17,22 23,27 C 8,25 3,11 12,11 z M 18,16 C 16,14 17,22 20,24 z"
    stroke-width="0.2"
    stroke="yellow"
    fill="currentColor"
    fill-rule="evenodd"
    transform="scale(1.4) rotate(45 16 16)"
/>
</symbol>
                """),
    ],
}

DEFAULT_WIDTH = 360
DEFAULT_HEIGHT = 600
DEFAULT_POINTS = 600

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
    seed = random.choice(seeds)
    q = deque([seed])
    pop = set([seed])
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
    content = [symbol for i in symbols.values() for name, symbol in i]
    content.extend([
        use.format(klass=name, name=name, point=point)
        for name, point in points
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
    spacing = args.spacing or [5]
    for n, (point, gap) in enumerate(
        poisson_disk(
            args.points,
            spacing,
            seeds=[complex(args.width / 2, args.height / 2)],
            top=complex(args.width, args.height)
        )
    ):
        name, symbol = random.choice(symbols[gap])
        scene.append((name, point))
        if args.debug:
            print(point, file=sys.stderr)

    print("{0} items".format(n), file=sys.stderr)
    print(paint(scene, args.width, args.height), file=sys.stdout)
    return 0

def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
