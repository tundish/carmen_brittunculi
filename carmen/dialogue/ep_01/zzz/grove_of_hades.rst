
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.types.version

:author: D Haynes
:date: 2018-04-11
:project: carmen
:version: |VERSION|

.. entity:: LOCATION
   :types: carmen.types.Location
   :states: carmen.types.Spot.grid_0804

.. entity:: PLAYER
   :types: carmen.types.Player
   :states: carmen.types.Spot.grid_0804

Grove of Hades
~~~~~~~~~~~~~~

Looking around
--------------

.. fx:: carmen.static.audio desolate-wind.mp3
   :offset: 0
   :duration: 25600
   :loop: 1

[LOCATION]_

    Here on the well-used path is a shrine to the god Hades.

[LOCATION]_

    The remains of offerings are scattered around.

Eve
---

.. condition:: PLAYER.state carmen.types.Time.eve

[LOCATION]_

    I move carefully round here at night.

Sunset
------

.. condition:: PLAYER.state carmen.types.Time.eve_sunset

[LOCATION]_

    Sometimes I hear voices. Sometimes no voices, only the
    chill of silent eyes watching from the dark.

Evening
-------

.. condition:: PLAYER.state carmen.types.Time.eve_evening

[LOCATION]_

    I move carefully round here at night.

Supper
------

.. condition:: PLAYER.state carmen.types.Time.eve_supper

[LOCATION]_

    Sometimes I hear voices. Sometimes no voices, only the
    chill of silent eyes watching from the dark.

Midnight
--------

.. condition:: PLAYER.state carmen.types.Time.eve_midnight

[LOCATION]_

    I move carefully round here at night.

Night
-----

.. condition:: PLAYER.state carmen.types.Time.eve_night

[LOCATION]_

    Sometimes I hear voices. Sometimes no voices, only the
    chill of silent eyes watching from the dark.

Predawn
-------

.. condition:: PLAYER.state carmen.types.Time.eve_predawn

[LOCATION]_

    I move carefully round here at night.

Dawn
----

.. condition:: PLAYER.state carmen.types.Time.eve_dawn

[LOCATION]_

    Sometimes I hear voices. Sometimes no voices, only the
    chill of silent eyes watching from the dark.

