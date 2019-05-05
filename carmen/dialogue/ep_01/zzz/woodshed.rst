
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.types.version

:author: D Haynes
:date: 2018-08-14
:project: carmen
:version: |VERSION|

.. entity:: LOCATION
   :types: carmen.types.Location
   :states: carmen.types.Spot.grid_1205

.. entity:: NARRATOR
   :types: carmen.types.Narrator

.. entity:: PLAYER
   :types: carmen.types.Player
   :states: carmen.types.Spot.grid_1205

Woodshed
~~~~~~~~

Theme
-----

.. fx:: carmen.static.audio demo_theme-slide_lead.mp3
   :offset: 0
   :duration: 26854
   :loop: 1

[LOCATION]_

    I'm standing in a shed.

Morning
-------

.. condition:: PLAYER.state carmen.types.Time.day_morning

[LOCATION]_

    A familiar place. My own place.

Dinner
------

.. condition:: PLAYER.state carmen.types.Time.day_dinner

[LOCATION]_

    Outside there is the sound of activity.

Night
-----

.. condition:: PLAYER.state carmen.types.Time.eve_night

[LOCATION]_

    There is wood in the air.

[LOCATION]_

    Two notes chime together.

[LOCATION]_

    One damp and of the earth. The other, dusty and dry.

[NARRATOR]_

    It is not yet light. I am dozing again.
