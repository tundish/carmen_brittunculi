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

spot = """
<circle cx="{0.real:.0}" cy="{0.imag:.0}" r="2"
stroke="gray" stroke-width="4"
fill="dimgrey"
/>
"""

WIDTH = 600
HEIGHT = 400

points = [complex(0, 0), complex(WIDTH, HEIGHT)]

def paint(points, width=WIDTH, height=HEIGHT):
    content = "\n".join(spot.format(point) for point in points)
    return svg.format(content, width=WIDTH, height=HEIGHT)

if __name__ == "__main__":
    sys.stdout.write(paint(points))
