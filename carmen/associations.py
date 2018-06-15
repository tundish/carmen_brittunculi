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


import collections

class Associations:

    def __init__(self):
        self.lookup = collections.OrderedDict([])

    def clear(self):
        for rels in self.lookup.values():
            for objs in rels.values():
                objs.clear()

    def ensemble(self, *args, **kwargs):
        return self.lookup.keys()

    def register(self, rel, primary, *args, **kwargs):
        subjects = set(args)
        for obj in {primary} | subjects:
            if obj not in self.lookup:
                self.lookup[obj] = collections.defaultdict(set)
        if rel is not None:
            self.lookup[primary][rel].update(subjects)
        return self

    def search(self, **kwargs):
        """
            Return objects matching all of the supplied parameter criteria.

        """
        return set(
            i for i in self.lookup.keys()
            if all(getattr(i, k, None) == v for k, v in kwargs.items())
        )

    def match(self, obj, forward=[], reverse=[], predicate=lambda x: True):
        """
            Return objects related to `obj` by at least one of the supplied
            relationships.

            :param forward: A sequence of forward relationships
            :param reverse: A sequence of reverse relationships
            :param predicate: A function with a single argument to filter matches

        """
        return {
            match for rel in forward for match in self.lookup[obj][rel]
            if predicate(match)
        } | {
            match
            for match in self.lookup
            for rel in reverse
            if predicate(match) and obj in self.lookup[match][rel]
        }
