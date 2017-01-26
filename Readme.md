Goal
====

There are many ways to handle processes (regarding starting, stopping, I/O).


Rules:
* print all lines from stdout and stderr on stdout of every started process 
* output must be done in main thread
* print logging only on stderr (to be able to wc / diff output)
* output of processes should be deterministic (to be able to wc/ diff output)


File:
* processes.json: *processes to run*
* example_process.py *an example python process with lots of output*
* pmgr_multithread_poll.py
* pmgr_singlethread_select.py

