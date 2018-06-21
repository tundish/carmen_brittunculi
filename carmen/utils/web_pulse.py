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

import aiohttp.web

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


print("Beats per minute: {0}".format(BPM))
print("Rate: {0} crotchets per sec".format(BPM / 60))
print("Seconds per measure: {0:0.3}".format(4 / BPM * 60))
print("Seconds per frame: {0:0.3}".format(8 * 4 / BPM * 60))
print("Frames per game: {0:0.2f}".format(4 * 60 * 60 / 8 / 4 * BPM / 60))
app = configure_app()
aiohttp.web.run_app(app)
