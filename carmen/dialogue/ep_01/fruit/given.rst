
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.logic.version

:author: D Haynes
:date: 2019-02-13
:project: carmen
:version: |VERSION|

.. entity:: PLAYER
   :types: carmen.types.Player
   :states: carmen.types.Spot.grid_1308

.. entity:: NARRATOR
   :types: carmen.types.Narrator

.. entity:: CADI
   :types: carmen.types.Innkeeper
   :states: carmen.types.Spot.grid_1308

.. entity:: OBJECTIVE
   :types: carmen.types.Collectable
   :states: carmen.types.Spot.pockets
            carmen.types.Visibility.visible

Mission
~~~~~~~

Handing it over
---------------

[CADI]_

    Thank you, |PLAYER|.

    Yet I need more.

.. property:: OBJECTIVE.state carmen.types.Spot.grid_1308
.. property:: OBJECTIVE.state carmen.types.Visibility.hidden

.. |OBJECT| property:: OBJECTIVE.__class__.__name__
.. |PLAYER| property:: PLAYER.name.firstname
