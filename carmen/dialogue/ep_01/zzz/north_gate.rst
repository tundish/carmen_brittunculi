
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
   :states: carmen.logic.Spot.grid_1109

.. entity:: PLAYER
   :types: carmen.logic.Player
   :states: carmen.logic.Spot.grid_1109

North gate
~~~~~~~~~~

Looking around
--------------

.. fx:: carmen.static.audio desolate-wind.mp3
   :offset: 0
   :duration: 25600
   :loop: 1

[LOCATION]_

    The track runs out from mud on to rock. This is the
    start of the road North.

Eve
---

.. condition:: PLAYER.state carmen.types.Time.eve

[LOCATION]_

    It is barred at night, but I can clamber over.
    The drop on the other side is tricky in the dark.

Sunset
------

.. condition:: PLAYER.state carmen.types.Time.eve_sunset

[LOCATION]_

    It is barred at night, but I can clamber over.
    The drop on the other side is tricky in the dark.

Evening
-------

.. condition:: PLAYER.state carmen.types.Time.eve_evening

[LOCATION]_

    It is barred at night, but I can clamber over.
    The drop on the other side is tricky in the dark.

Supper
------

.. condition:: PLAYER.state carmen.types.Time.eve_supper

[LOCATION]_

    It is barred at night, but I can clamber over.
    The drop on the other side is tricky in the dark.

Midnight
--------

.. condition:: PLAYER.state carmen.types.Time.eve_midnight

[LOCATION]_

    It is barred at night, but I can clamber over.
    The drop on the other side is tricky in the dark.

Night
-----

.. condition:: PLAYER.state carmen.types.Time.eve_night

[LOCATION]_

    It is barred at night, but I can clamber over.
    The drop on the other side is tricky in the dark.

Predawn
-------

.. condition:: PLAYER.state carmen.types.Time.eve_predawn

[LOCATION]_

    It is barred at night, but I can clamber over.
    The drop on the other side is tricky in the dark.

Dawn
----

.. condition:: PLAYER.state carmen.types.Time.eve_dawn

[LOCATION]_

    It is barred at night, but I can clamber over.
    The drop on the other side is tricky in the dark.

