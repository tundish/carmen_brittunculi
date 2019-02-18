
..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

.. |VERSION| property:: carmen.logic.version

:author: D Haynes
:date: 2019-02-14
:project: carmen
:version: |VERSION|

.. entity:: PLAYER
   :types: carmen.logic.Player
   :states: carmen.logic.Spot.grid_1308
            carmen.logic.Time.eve

.. entity:: CADI
   :types: carmen.logic.Character

Reminder
~~~~~~~~

.. Consider dialogue conditional on Cadi's spot.

Cadi's advice
-------------

[CADI]_

    Be sure to keep the pattern I taught you.

    We stack the wet logs at the end where the wind comes in.

[CADI]_

    Before Bryn comes here with new wood, you must pile up the dry
    logs in the Kitchen.
    
[CADI]_

    Hah, it's done already!

    |PLAYER| you're the only one I trust.

.. |PLAYER| property:: PLAYER.name.firstname
