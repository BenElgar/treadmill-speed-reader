Treadmill Speed Reader
======================

The Treadmill Speed Reader allows a user to measure the speed of a York Pacer 2120 Treadmill by intercepting the two wires leading from the magnets on the right hand side up to the handle bars.


Running
-------

Readings can be streamed over the network by executing `run.py`. By default this uses port 12229. An example of how to receive treadmill data can be seen in `TreadmillReceive.py`.

Recording
---------

Readings can be recorded by executing `record.py` and passing it the name of a log file to which the recording should be saved.

Playback
--------

Recordings can be played back by executing `simulate.py` and passing it the name of a log file to which the recording is saved. The packaged `slow.log` file is an example of such a log file.



