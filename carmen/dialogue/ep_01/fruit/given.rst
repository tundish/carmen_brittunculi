
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.types.version

:author: D Haynes
:date: 2019-02-13
:project: carmen
:version: |VERSION|

.. entity:: PLAYER
   :types: carmen.types.Player
   :states: carmen.types.Spot.grid_1206

.. entity:: NARRATOR
   :types: carmen.types.Narrator

.. entity:: CADI
   :types: carmen.types.Innkeeper
   :states: carmen.types.Spot.grid_1206

.. entity:: OBJECTIVE
   :types: carmen.types.Collectable
   :states: carmen.types.Spot.pockets
            carmen.types.Visibility.visible

Mission
~~~~~~~

Handing it over
---------------

.. fx:: carmen.static.audio  VOC_190403-0017-warm.mp3
   :offset: 0
   :duration: 15386
   :loop: 1

[CADI]_

    Thank you, |PLAYER|.

    We're always short of |OBJECT| s.

[NARRATOR]_

    She gets back to her work, humming to herself.

[CADI]_

    Find some more for me if you can, please.

.. property:: OBJECTIVE.state carmen.types.Spot.grid_1206
.. property:: OBJECTIVE.state carmen.types.Visibility.hidden

.. |OBJECT| property:: OBJECTIVE.__class__.__name__
.. |PLAYER| property:: PLAYER.name.firstname
