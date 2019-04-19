
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.logic.version

:author: D Haynes
:date: 2018-07-02
:project: carmen
:version: |VERSION|

.. entity:: PLAYER
   :types: carmen.types.Player

.. entity:: NARRATOR
   :types: carmen.types.Narrator

.. entity:: LOCATION
   :types: carmen.types.Location
   :states: carmen.types.Visibility.detail

.. entity:: OBJECTIVE
   :types: carmen.types.Collectable
   :states: carmen.types.Spot.grid
            carmen.types.Visibility.visible

Found
~~~~~

An item claimed
---------------

.. fx:: carmen.static.audio  VOC_190403-0017-super.mp3
   :offset: 0
   :duration: 18756
   :loop: 1

[NARRATOR]_

    You pick up a |OBJECT|.

.. property:: OBJECTIVE.state carmen.types.Spot.pockets

.. |OBJECT| property:: OBJECTIVE.__class__.__name__
