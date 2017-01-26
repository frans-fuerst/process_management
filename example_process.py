#!/usr/bin/env python3

import time
import os
import sys

def main():
    t0 = time.time()
    pid = os.getpid()
    for i in range(500):
        x = 0
        if '--sleep' in sys.argv:
            time.sleep(i / 10000)
        else:
            tn = time.time()
            for j in range(10*i):
                x = x + i / i
        tn = time.time() - t0
        print("%d; std; %d; %.2f" % (pid, i, tn), file=sys.stdout)
        print("%d; err; %d; %.2f" % (pid, i, tn), file=sys.stderr)

if __name__ == '__main__':
    main()
