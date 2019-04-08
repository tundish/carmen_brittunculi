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

import argparse
import asyncio
import configparser
import functools
import logging
import os
import pathlib
import pkg_resources
import signal
import sys


class Config:

    @classmethod
    def load(cls, name):
        log = logging.getLogger("carmen.config")
        path, data = cls.find_file(name)
        cfg = cls.parser()
        cfg.read_string(data, source=path)
        log.info("Loaded '{0!s}'".format(path))
        cls.path = path
        cls.cfg = cfg
        return cls.path, cls.cfg

    @staticmethod
    def find_file(name):
        if not name:
            return (
                pathlib.Path(pkg_resources.resource_filename("carmen", "data/demo.cfg")).resolve(),
                pkg_resources.resource_string("carmen", "data/demo.cfg").decode("utf8")
            )
        else:
            with open(name, "r") as fObj:
                return (pathlib.Path(fObj.name).resolve(), fObj.read())

    @staticmethod
    def parser():
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        return cfg


async def do_regularly(msg, period=3):
    while True:
        print(os.getpid(), msg)
        await asyncio.sleep(period)


def parser():
    p = argparse.ArgumentParser(
        prog="signals.main.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__
    )
    p.add_argument("--config", default=None, help="Specify a config file")
    return p


def main(args):
    path, cfg = Config.load(args.config)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, functools.partial(loop.call_soon, loop.stop))
    loop.add_signal_handler(signal.SIGTERM, functools.partial(loop.call_soon, loop.stop))
    loop.add_signal_handler(
        signal.SIGHUP, functools.partial(loop.call_soon, Config.load, args.config)
    )

    jobs = [
        loop.create_task(do_regularly("ping", 3)),
        loop.create_task(do_regularly("wobble", 17))
    ]
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        for job in jobs:
            job.cancel()
        loop.call_soon(loop.stop)


if __name__ == "__main__":
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)
