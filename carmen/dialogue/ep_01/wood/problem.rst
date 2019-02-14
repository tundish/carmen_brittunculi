
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
   :states: carmen.logic.Time.day_noon

.. entity:: NARRATOR
   :types: carmen.logic.Narrator
   :states: 104

Problem
~~~~~~~

Inner voice
-----------

[NARRATOR]_

    You cannot give the miners wood.

    They do not know it. They will send up smoke.

    Then Harac will send his people over the river to take us.

[NARRATOR]_

    The miners know of Harac. Some are of his family.

    None of them want to see him again.

.. property:: NARRATOR.state 105
