
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

.. entity:: NPC
   :types: carmen.logic.Character

.. entity:: LOCATION
   :types: carmen.logic.Location
   :states: carmen.types.Visibility.detail

.. entity:: DESTINATION
   :types: carmen.logic.Location
   :states: carmen.types.Visibility.indicated

.. entity:: OBJECTIVE
   :states: carmen.types.Visibility.new

Mission
~~~~~~~

Something to do
---------------

[NPC]_

    I've got something for you to do.

[NPC]_

    Have a look around the |PLACE|.
    You might find a |OBJECT|.

[NPC]_

    Come back to the |HERE| when you've got one.

.. |OBJECT| property:: OBJECTIVE.__class__.__name__
.. |PLACE| property:: DESTINATION.label
.. |HERE| property:: LOCATION.label
