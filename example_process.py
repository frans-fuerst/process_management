#!/usr/bin/env python3

import time
import os
import sys

def main():
    t0 = time.time()
    pid = os.getpid()
    for i in range(1000):
        x = 0
        if True:
            tn = time.time()
            for j in range(10*i):
                x = x + i / i
        else:
            time.sleep(i/1000)
        tn = time.time() - t0
        print("%d; std; %d; %.2f %d" % (pid, i, tn, x), file=sys.stdout)
        print("%d; err; %d; %.2f" % (pid, i, tn), file=sys.stderr)

if __name__ == '__main__':
    main()
