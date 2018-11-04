
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.logic.version

:author: D Haynes
:date: 2018-10-22
:project: carmen
:version: |VERSION|

.. entity:: LOCATION
   :types: carmen.logic.Location
   :states: carmen.logic.Spot.grid_1308

.. entity:: PLAYER
   :types: carmen.logic.Player
   :states: carmen.logic.Spot.grid_1308
            carmen.logic.Time.eve_dawn

.. entity:: NARRATOR
   :types: carmen.logic.Narrator

.. entity:: CADI
   :types: carmen.logic.Character

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
