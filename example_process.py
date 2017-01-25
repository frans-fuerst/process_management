#!/usr/bin/env python3

import time
import os
import sys

def main():
    t0 = time.time()
    pid = os.getpid()
    for i in range(100):
        time.sleep(i/1000)
        tn = time.time() - t0
        print("%d; std; %d; %.2f" % (pid, i, tn), file=sys.stdout)
        print("%d; err; %d; %.2f" % (pid, i, tn), file=sys.stderr)

if __name__ == '__main__':
    main()
