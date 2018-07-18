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
from decimal import Decimal
import itertools

import aiohttp.web
import pygal

# Text reveal with CSS3:
# https://www.youtube.com/watch?v=3YKpKpC1O5s

# Animations
# https://www.creativebloq.com/inspiration/css-animation-examples

# Z-index slideshow:
# https://www.youtube.com/watch?v=z74ExMz-cWU

BPM = 90

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return aiohttp.web.Response(text=text)

def configure_app():
    app = aiohttp.web.Application()
    app.router.add_routes([
        aiohttp.web.get('/', handle),
        aiohttp.web.get('/{name}', handle)
    ])
    return app

def oscillator(damping):
    damping = float(damping)
    weight  =  0.1
    value   =  0.0
    middle  = value

    yield 0, 0

    while True:
        if value > middle:
            weight -= damping
        else:
            weight += damping

        value += weight

        yield value, weight

def delay(gain=1.2, init=(1, 1)):
    buf = deque([Decimal(i) for i in init])
    gain = Decimal(gain)
    while True:
        val = buf.popleft()
        yield val
        buf.append(gain * buf[-1] - val)

print("Beats per minute: {0}".format(BPM))
print("Rate: {0} crotchets per sec".format(BPM / 60))
print("Seconds per measure: {0:0.3}".format(4 / BPM * 60))
print("Seconds per frame: {0:0.3}".format(8 * 4 / BPM * 60))
print("Frames per game: {0:0.2f}".format(4 * 60 * 60 / 8 / 4 * BPM / 60))

#print(*list(itertools.islice(oscillator(0.1), 0, 12)))
data = itertools.islice(delay(), 0, 124)
# app = configure_app()
# aiohttp.web.run_app(app)

chart = pygal.XY()
chart.title = "Wave"
chart.add("delay osc", list(enumerate(data)))
chart.render_in_browser()

