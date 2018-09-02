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

import logging


class Play:
    """ TODO: Move to turberfield-dialogue """

    _fields = []

    def __init__(self, **kwargs):
        for name in self._fields:
            setattr(self, name, kwargs.pop(name, None))

        super().__init__(**kwargs)

    def __call__(self, folder, index, references, *args, **kwargs) -> dict:
        return folder.metadata

class Session(Play):

    _fields = ["uid", "player", "frames", "interlude", "finder", "workers"]

    class Registry:

        operations = []

        @classmethod
        def register(cls):
            def decorator(method):
                cls.operations.append(method)
                return method
            return decorator

    def __call__(self, folder, index, references, *args, until=None, **kwargs) -> dict:
        rv = {}
        for function in self.Registry.operations:
            if function.__name__ == until:
                break
            else:
                rv.update(function(self, folder, index, references, **kwargs))
        return rv

    @Registry.register()
    def day_night_cycle(self, *args, log=None, loop=None, **kwargs):
        log = log or logging.getLogger(str(self.uid))
        rv = {}
        log.info(rv)
        return rv
