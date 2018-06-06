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
}
WIDTH = 800
HEIGHT = 360

def overlaps(this, that, span):
    return cmath.isclose(this, that, abs_tol=span)

def sow(seed, min_dist, max_dist):
    r = random.uniform(min_dist, max_dist)
    phi = random.uniform(0, 2 * cmath.pi)
    return seed + cmath.rect(r, phi)

def poisson_disk(
    n_points, gaps, seeds,
    n_gen=12, min_dist=16, max_dist=42,
    origin=complex(0, 0), top=complex(WIDTH, HEIGHT)
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

def paint(points, width=WIDTH, height=HEIGHT):
    content = [symbol for i in symbols.values() for name, symbol in i]
    content.extend([
        use.format(klass=name, name=name, point=point)
        for name, point in points
    ])
    return svg.format("\n".join(content), width=WIDTH, height=HEIGHT)


if __name__ == "__main__":

    scene = []
    for n, (point, gap) in enumerate(
        poisson_disk(6000, [5], [complex(WIDTH / 2, HEIGHT / 2)])
    ):
        name, symbol = random.choice(symbols[gap])
        scene.append((name, point))
        print(point, file=sys.stderr)

    print("{0} items".format(n), file=sys.stderr)
    print(paint(scene), file=sys.stdout)
