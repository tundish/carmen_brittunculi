
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.types.version

:author: D Haynes
:date: 2018-07-02
:project: carmen
:version: |VERSION|

.. entity:: PLAYER
   :types: carmen.types.Player

.. entity:: NARRATOR
   :types: carmen.types.Narrator

.. entity:: OBJECTIVE
   :states: carmen.types.Visibility.visible

Mission
~~~~~~~

Something to do
---------------

[Narrator]_

    You pick up the |OBJECT|.

.. property:: OBJECTIVE.state carmen.types.Spot.pockets

.. |OBJECT| property:: OBJECTIVE.__class__.__name__
