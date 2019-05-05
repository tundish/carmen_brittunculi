
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.types.version

:author: D Haynes
:date: 2018-10-22
:project: carmen
:version: |VERSION|

.. entity:: PLAYER
   :types: carmen.types.Player
   :states: carmen.types.Spot.grid_1206
            carmen.types.Time.eve

.. entity:: NARRATOR
   :types: carmen.types.Narrator

.. entity:: CADI
   :types: carmen.types.Innkeeper
   :states: carmen.types.Spot.grid_1206

In the kitchen
~~~~~~~~~~~~~~

Waking
------

[NARRATOR]_

    She has taken the skin from the chimney.

    The wood is alight, crackling.

[CADI]_

    The sun is not up, but here is my sunshine!

[NARRATOR]_

    There is light in her eyes. Orange and red. Dancing.

[CADI]_

    Wait for the dawn, |PLAYER|. Then do you look for the apples again?

.. |PLAYER| property:: PLAYER.name.firstname
