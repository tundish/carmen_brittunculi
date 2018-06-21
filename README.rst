..  Titling
    ##++::==~~--''``

Carmen Brittunculi
++++++++++++++++++

This is a piece of work for the `Roman Mytholojam 2018`_ Game Jam.

Source Code
:::::::::::

The code is licenced under the `GNU Affero General Public License`_.
Dialogue scripts are copyright the author.

You can get the source by cloning the `Github repository`_.

Installation
============

This is an installable Python package.

#. Install `python3` using your OS package manager.
#. Create a new Python virtual environment::

    python3 -m venv ~/py3

#. Download the code::

    git clone git@github.com:tundish/carmen_brittunculi.git

#. Change directory::

    cd carmen_brittunculi

#. Install the game package::

    ~/py3/bin/pip install .

#. Launch the game server::

    ~/py3/bin/carmen-web

#. Play the game in your browser::

    firefox localhost:8080

Downloads
:::::::::

Standalone installable binaries may be available at the `Itch.io project page`_.

Notes
:::::

The game is not yet finished. Here are some references and technologies
which have inspired it so far:

* `Turberfield Dialogue`_ library.
* Lisa Brown's `Nuance of Juice`_.
* `SVG coordinates`_ within HTML.
* `Post-Roman scenario`_ from an abandoned project.
* `Mammy apple`_ tree.

The web framework is `aiohttp`.
Development uses Aiohttp version 2, but avoiding `impediments to using version 3`_.

.. _Roman Mytholojam 2018: https://itch.io/jam/roman-mytholojam
.. _GNU Affero General Public License: http://www.gnu.org/licenses/agpl.html
.. _Itch.io project page: https://tundish.itch.io/carmen-brittunculi
.. _Github repository: https://github.com/tundish/carmen_brittunculi
.. _Nuance of Juice: https://www.youtube.com/watch?v=qtgWBUIOjK4
.. _Turberfield Dialogue: http://pythonhosted.org/turberfield-dialogue/
.. _Post-Roman scenario: http://pythonhosted.org/turberfield-eargain/guide.html
.. _Mammy apple: https://en.wikipedia.org/wiki/Mammea_americana
.. _SVG coordinates: https://www.sarasoueidan.com/blog/svg-coordinate-systems/
.. _impediments to using version 3: https://docs.aiohttp.org/en/stable/changes.html#id147
