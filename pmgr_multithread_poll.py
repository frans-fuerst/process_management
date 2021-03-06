#!/usr/bin/env python3

""" demonstrate multithread based process managing with performance,
    readablity and complexity in mind
"""

import subprocess
import threading
import functools
import select
import json
import time
import sys


class process_handler:

    def __init__(self, name: str, cmd: list):
        print('start: %s' % cmd, file=sys.stderr)
        self._name = '%s(%s)' % (name, ' '.join(cmd))
        self._thread = threading.Thread(target=lambda: self._start(cmd),
                                        daemon=True)
        self._thread.start()

    def __repr__(self):
        return self._name

    def _start(self, cmd: list):
        self._process = subprocess.Popen(
            args=cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0)

        _to_poll = [self._process.stdout,
                    self._process.stderr]

        def output_line(stream: str, line: bytes) -> None:
            # here we should invoke a main thread callable
            print('%s: %s' % (stream, line.decode().strip('\n')))

        while self._process.poll() is None:
            for d in select.select(_to_poll, [], [])[0]:
                if d == self._process.stdout:
                    output_line('stdout', d.readline())
                if d == self._process.stderr:
                    output_line('stderr', d.readline())

        # process is not running any more - read messages in the
        # buffers and terminate the read loop
        for l in self._process.stdout.readlines():
            output_line('stdout', l)
        for l in self._process.stderr.readlines():
            output_line('stderr', l)

        self._process.wait()

    def wait(self):
        self._thread.join()


def main():
    processes = []
    t0 = time.time()
    for l in json.load(open('processes.json'), encoding='utf-8'):
        for _ in range(l['count']):
            processes.append(process_handler(
                                name='p%d' % len(processes),
                                cmd=l['cmd']))

    print('start up took %.1fms' % ((time.time() - t0) * 1000),
          file=sys.stderr)

    for p in processes:
        print('wait for %r' % p)
        p.wait()

    print('execution took %.1fms' % ((time.time() - t0) * 1000),
          file=sys.stderr)


if __name__ == '__main__':
    main()