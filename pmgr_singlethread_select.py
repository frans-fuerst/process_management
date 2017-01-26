#!/usr/bin/env python3

import subprocess
import select
import json
import time


class fd_handler:
    def __init__(self):
        self._fds = {}

    def register(self, fd: int, cb: callable) -> None:
        self._fds[fd] = cb

    def unregister(self, fd: int) -> None:
        del self._fds[fd]

    def wait_and_process(self):
        for _fd in select.select(self._fds.keys(), [], [])[0]:
#            t = time.time()
            self._fds[_fd]()
#            d = time.time() - t
#            print('callback took %.1fms' % (d * 1000))

    def size(self) -> int:
        return len(self._fds)


class process_handler:
    def __init__(self, name: str, cmd: list, fd_handler: fd_handler):
        print('start: %s' % cmd)
        self._name = '%s(%s)' % (name, ' '.join(cmd))
        self._fd_handler = fd_handler
        self._process = subprocess.Popen(args=cmd, stdout=subprocess.PIPE)
        self._fd_handler.register(self._process.stdout.fileno(), self._read_stdout)

    def __repr__(self):
        return self._name

    def _handle_program_termination(self):
        if self._process.poll() is None:
            return False
        self._fd_handler.unregister(self._process.stdout.fileno())
        return True

    def _read_stdout(self):
        if self._handle_program_termination():
            return

        _line = self._process.stdout.readline().decode()
        if _line == '':
            return

        print(_line.strip('\n'))


def main():
    fds = fd_handler()
    processes = []

    t0 = time.time()
    for l in json.load(open('processes.json'), encoding='utf-8'):
        for c in range(l['count']):
            try:
                processes.append(process_handler(
                                    name='p%d' % len(processes), 
                                    cmd=l['cmd'],
                                    fd_handler=fds))
            except FileNotFoundError:
                print('could not start %s' % l)

    print('start up took %.1fms' % ((time.time() - t0) * 1000))

    while fds.size() > 0:
#        print('main loop, fd size = %d' % fds.size())
        fds.wait_and_process()

    print('execution took %.1fms' % ((time.time() - t0) * 1000))

if __name__ == '__main__':
    main()

