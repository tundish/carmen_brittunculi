
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

.. entity:: NARRATOR
   :types: carmen.types.Narrator

Goodbye
~~~~~~~

Curtain
-------

.. fx:: carmen.static.audio  VOC_190403-0017-super.mp3
   :offset: 0
   :duration: 18756
   :loop: 1

[NARRATOR]_

    Thanks for playing, |PLAYER|.

    You've reached the end of Carmen Brittunculi version |VERSION|.

.. |PLAYER| property:: PLAYER.name.firstname
