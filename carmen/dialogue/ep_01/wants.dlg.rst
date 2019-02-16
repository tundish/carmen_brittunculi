
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.logic.version

:author: D Haynes
:date: 2018-09-11
:project: carmen
:version: |VERSION|

.. entity:: PLAYER
   :types: carmen.logic.Player
   :states: carmen.types.Wants.needs

.. entity:: NARRATOR
   :types: carmen.logic.Narrator

.. entity:: LOCATION
   :types: carmen.logic.Location
   :states: carmen.types.Visibility.detail

Looking after yourself
~~~~~~~~~~~~~~~~~~~~~~

Hungry
------

.. condition:: PLAYER.state carmen.types.Wants.needs_food

[NARRATOR]_

    You're hungry.


Tired
-----

.. condition:: PLAYER.state carmen.types.Wants.needs_sleep

[NARRATOR]_

    You're tired.

.. |HERE| property:: LOCATION.label
