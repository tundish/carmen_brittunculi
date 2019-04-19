
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.logic.version

:author: D Haynes
:date: 2018-04-11
:project: carmen
:version: |VERSION|

.. entity:: LOCATION
   :types: carmen.logic.Location
   :states: carmen.logic.Spot.grid_1306

.. entity:: PLAYER
   :types: carmen.logic.Player
   :states: carmen.logic.Spot.grid_1306

Common house
~~~~~~~~~~~~

Atmosphere
----------

.. condition:: PLAYER.state carmen.types.Wants.needs_sleep

.. fx:: carmen.static.audio  VOC_190403-0017-bluegrass.mp3
   :offset: 0
   :duration: 19513
   :loop: 1


Looking around
--------------

[LOCATION]_

    You stand within a large circular structure. It is built of
    wood and thatch. This is a common house for shelter and storage.

[LOCATION]_

    The ground about is deeply rutted. Straw binds the pathway past
    the Common House.

