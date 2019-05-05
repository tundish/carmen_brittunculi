
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.types.version

:author: D Haynes
:date: 2019-02-19
:project: carmen
:version: |VERSION|

.. entity:: PLAYER
   :types: carmen.types.Player
   :states: carmen.types.Spot.grid_1206

.. entity:: CADI
   :types: carmen.types.Innkeeper

.. entity:: NARRATOR
   :types: carmen.types.Narrator

.. entity:: DESTINATION
   :types: carmen.types.Location
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
