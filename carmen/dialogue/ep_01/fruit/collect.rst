
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

.. entity:: NPC
   :types: carmen.types.Character

.. entity:: LOCATION
   :types: carmen.types.Location
   :states: carmen.types.Visibility.detail

.. entity:: TARGET
   :types: carmen.types.Location
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

    Come back to the Kitchen when you've got one.

.. property:: OBJECTIVE.state carmen.types.Visibility.visible

.. condition:: PLAYER.state carmen.types.Time.eve

[NPC]_

    Be careful in the dark, |PLAYER| !


.. |OBJECT| property:: OBJECTIVE.__class__.__name__
.. |PLACE| property:: TARGET.label
.. |PLAYER| property:: PLAYER.name.firstname
