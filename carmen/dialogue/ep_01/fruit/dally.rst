
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.logic.version

:author: D Haynes
:date: 2019-02-19
:project: carmen
:version: |VERSION|

.. entity:: PLAYER
   :types: carmen.logic.Player
   :states: carmen.logic.Spot.grid_1206

.. entity:: CADI
   :types: carmen.logic.Innkeeper

.. entity:: NARRATOR
   :types: carmen.logic.Narrator

.. entity:: DESTINATION
   :types: carmen.logic.Location
   :states: carmen.types.Visibility.indicated

Prevarication
~~~~~~~~~~~~~

What are you waiting for
------------------------

.. fx:: carmen.static.audio  VOC_190402-0014-horns.mp3
   :offset: 0
   :duration: 18599
   :loop: 1

[NARRATOR]_

    She tends the fire.

[CADI]_

    You should go over to the |PLACE|, |PLAYER|. 

.. |PLAYER| property:: PLAYER.name.firstname
.. |PLACE| property:: DESTINATION.label
