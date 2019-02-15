
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

.. entity:: NARRATOR
   :types: carmen.types.Narrator

.. entity:: PLAYER
   :types: carmen.logic.Player
   :states: carmen.logic.Spot.grid_1407

Woodshed
~~~~~~~~

Looking around
--------------

.. condition:: PLAYER.state carmen.types.Wants.nothing

.. fx:: carmen.static.audio demo_theme-slide_lead.mp3
   :offset: 0
   :duration: 26000
   :loop: 1

[LOCATION]_

    In a familiar, high roofed place. There are stacks of bundled wood.

Time to leave
-------------

.. condition:: PLAYER.state carmen.types.Wants.needs_food

.. fx:: carmen.static.audio demo_theme-slide_lead.mp3
   :offset: 0
   :duration: 26000
   :loop: 1

[LOCATION]_

    In a familiar, high roofed place. There are stacks of bundled wood.

    Outside there is the sound of activity.

What's the hurry?
-----------------

.. condition:: PLAYER.state carmen.types.Wants.needs_sleep

.. fx:: carmen.static.audio demo_theme-slide_lead.mp3
   :offset: 0
   :duration: 26000
   :loop: 1

[LOCATION]_

    In a familiar, high roofed place. It smells of damp wood.

[NARRATOR]_

    It is not yet light. I doze again.
