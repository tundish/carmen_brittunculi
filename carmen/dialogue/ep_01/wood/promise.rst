
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.types.version

:author: D Haynes
:date: 2018-10-22
:project: carmen
:version: |VERSION|

.. entity:: LOCATION
   :types: carmen.types.Location
   :states: carmen.types.Spot.grid_1208

.. entity:: PLAYER
   :types: carmen.types.Player
   :states: carmen.types.Spot.grid_1208

.. entity:: NARRATOR
   :types: carmen.types.Narrator

.. entity:: ANT
   :types: carmen.types.Merchant

.. entity:: CADI
   :types: carmen.types.Character

Bryn and Cadi talk Wood
~~~~~~~~~~~~~~~~~~~~~~~

A question
----------

[ANT]_

    How was the wood today?

[CADI]_

    It took well. There was no smoke.

A correction
------------

[ANT]_

    No need to worry about smoke after dark. Save that dry wood for the day.

[CADI]_

    The wind is in the East. I dare not use the younger wood.

[ANT]_

    Why not?

[CADI]_

    It is of Larch. The smell would carry to him.

[ANT]_

    Hah! Harac cannot smell any Larchwood.

    His nose is flat across his face.

    He couldn't smell a rotten mule roasting in a pig-pen of Larch trees!

[CADI]_

    But one of them would smell it.

    So I only burn the wet Larch in the nights without a breeze.

A nudge
-------

[ANT]_

    Good progress. |PLAYER| knows something of the Wood.

[CADI]_

    Then next I'll teach the Ale.

[ANT]_

    Yes, |PLAYER| must learn the Ale. But Wood for now. There's more yet.

.. |PLAYER| property:: PLAYER.name.firstname
