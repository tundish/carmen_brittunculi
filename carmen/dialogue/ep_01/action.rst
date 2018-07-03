
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.logic.version

:author: D Haynes
:date: 2018-07-02
:project: carmen
:version: |VERSION|

.. entity:: PLAYER
   :types: carmen.logic.Player

.. entity:: NARRATOR
   :types: carmen.logic.Narrator

.. entity:: OBJECTIVE
   :states: carmen.types.Visibility.visible

Mission
~~~~~~~

Something to do
---------------

[Narrator]_

    You pick up the |OBJECT|.

.. |OBJECT| property:: OBJECTIVE.__class__.__name__
