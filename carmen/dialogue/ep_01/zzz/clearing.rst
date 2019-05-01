
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
   :states: carmen.logic.Spot.grid_1104

.. entity:: PLAYER
   :types: carmen.logic.Player
   :states: carmen.logic.Spot.grid_1104

Clearing
~~~~~~~~

Looking around
--------------

[LOCATION]_

    A narrow area is cleared of trees.

Sunrise
-------

.. condition:: PLAYER.state carmen.types.Time.day_sunrise

[LOCATION]_

   Between the low stumps which remain, span narrow bridges across
   the muddy mess below.

Early
-----

.. condition:: PLAYER.state carmen.types.Time.day_early

[LOCATION]_

   If you don't want to step in the mud, you can hop from stump to stump.

Breakfast
---------

.. condition:: PLAYER.state carmen.types.Time.day_breakfast

[LOCATION]_

   Between the low stumps which remain, span narrow bridges across
   the muddy mess below.

Morning
-------

.. condition:: PLAYER.state carmen.types.Time.day_morning

[LOCATION]_

   If you don't want to step in the mud, you can hop from stump to stump.

Noon
----

.. condition:: PLAYER.state carmen.types.Time.day_noon

[LOCATION]_

   Between the low stumps which remain, span narrow bridges across
   the muddy mess below.

Lunch
-----

.. condition:: PLAYER.state carmen.types.Time.day_lunch

[LOCATION]_

   If you don't want to step in the mud, you can hop from stump to stump.

Afternoon
---------

.. condition:: PLAYER.state carmen.types.Time.day_afternoon

[LOCATION]_

   Between the low stumps which remain, span narrow bridges across
   the muddy mess below.

Dinner
------

.. condition:: PLAYER.state carmen.types.Time.day_dinner

[LOCATION]_

   If you don't want to step in the mud, you can hop from stump to stump.

Dusk
----

.. condition:: PLAYER.state carmen.types.Time.day_dusk

[LOCATION]_

   Between the low stumps which remain, span narrow bridges across
   the muddy mess below.

Eve
---

.. condition:: PLAYER.state carmen.types.Time.eve

[LOCATION]_

   If you don't want to step in the mud, you can hop from stump to stump.

Sunset
------

.. condition:: PLAYER.state carmen.types.Time.eve_sunset

[LOCATION]_

   I slip and stumble across.

Evening
-------

.. condition:: PLAYER.state carmen.types.Time.eve_evening

[LOCATION]_

   They have spread out old bales of wool to soak up the mire.

Supper
------

.. condition:: PLAYER.state carmen.types.Time.eve_supper

[LOCATION]_

   I slip and stumble across.

Midnight
--------

.. condition:: PLAYER.state carmen.types.Time.eve_midnight

[LOCATION]_

   They have spread out old bales of wool to soak up the mire.

Night
-----

.. condition:: PLAYER.state carmen.types.Time.eve_night

[LOCATION]_

   I slip and stumble across.

Predawn
-------

.. condition:: PLAYER.state carmen.types.Time.eve_predawn

[LOCATION]_

   They have spread out old bales of wool to soak up the mire.

Dawn
----

.. condition:: PLAYER.state carmen.types.Time.eve_dawn

[LOCATION]_

   I slip and stumble across.

