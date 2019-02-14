
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.logic.version

:author: D Haynes
:date: 2018-08-14
:project: carmen
:version: |VERSION|

.. entity:: LOCATION
   :types: carmen.logic.Location
   :states: carmen.logic.Spot.grid_1407

.. entity:: PLAYER
   :types: carmen.logic.Player
   :states: carmen.logic.Spot.grid_1407

Woodshed
~~~~~~~~

Looking around
--------------

.. condition:: PLAYER.state carmen.types.Time.day

[LOCATION]_

    You are in a high roofed place. There are stacks of bundled wood.

Bumping into things
-------------------

.. condition:: PLAYER.state carmen.types.Time.eve

[LOCATION]_

    You are in a high roofed place. It smells of damp wood.

