mule-frans (armv7/single/800, Python 3.5.1)

    10 x `find /etc`
        pmgr_multithread_poll.py
            3982.2ms 3992.7ms 3870.0ms

        pmgr_singlethread_select.py
            511.6ms 474.9ms 479.2ms

    5 x example_process
        pmgr_multithread_poll.py
            27824.2ms 27830.5ms 27813.9ms

        pmgr_singlethread_select.py
            22611.5ms 22650.9ms 22468.0ms

    5 x example_process --sleep

        time ./pmgr_multithread_poll.py
            17710.3ms | real 0m19.010s, user 0m8.398s, sys 0m2.405s

        time ./pmgr_singlethread_select.py 
            16610.8ms | real 0m17.916s, user 0m7.227s, sys 0m1.945s

i5-3570K
