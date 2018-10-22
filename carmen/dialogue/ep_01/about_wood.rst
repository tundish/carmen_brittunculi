
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

.. entity:: NARRATOR
   :types: carmen.logic.Narrator

.. entity:: BRYN
   :types: carmen.logic.Character

.. entity:: CADI
   :types: carmen.logic.Character

Bryn and Cadi talk Wood
~~~~~~~~~~~~~~~~~~~~~~~

A question
----------

[BRYN]_

    How was the wood today?

[CADI]_

    It took well. There was no plume.

A correction
------------

[BRYN]_

    Care not for smoke after dark. Save that dry wood for the day.

[CADI]_

    The wind is in the East. I dare not use the younger wood.

[BRYN]_

    Why then?

[CADI]_

    It is of Larch. The smell would carry to him.

[BRYN]_

    Hah! Brock cannot smell any Larchwood.

    His nose is flat across his face.

    He cannot smell a fallen mule roasting in a quarry pit of Larch trees.

[CADI]_

    But one of them would smell it.

    I only burn the wet Larch in the eve without breeze.

A nudge
-------

[BRYN]_

    Good so. |PLAYER| knows well the Wood.

[CADI]_

    Then next I teach the Ale?

[BRYN]_

    Yes, |PLAYER| must learn the Ale. But Wood for now.

.. |PLAYER| property:: PLAYER.name.firstname
