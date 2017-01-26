#!/usr/bin/env python3

import subprocess
import select
import json
import time
import sys


class fd_handler:
    def __init__(self):
        self._fds = {}

    def register(self, fd: int, cb: callable) -> None:
        self._fds[fd] = cb

    def unregister(self, fd: int) -> None:
        _new_fds = dict(self._fds)
        del _new_fds[fd]
        self._fds = _new_fds

    def wait_and_process(self) -> None:
        _fds = self._fds
        for _fd in select.select(_fds.keys(), [], [])[0]:
            _fds[_fd](_fd)

    def size(self) -> int:
        return len(self._fds)


class process_handler:
    def __init__(self, name: str, cmd: list, fdhandler: fd_handler):
        print('start: %s' % cmd)
        self._name = '%s(%s)' % (name, ' '.join(cmd))
        self._fd_handler = fdhandler
        self._process = subprocess.Popen(
            args=cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0)
        self._fd_handler.register(
            self._process.stdout,
            lambda stream: self._read_stream('stdout', stream))
        self._fd_handler.register(
            self._process.stderr,
            lambda stream: self._read_stream('stderr', stream))

    def __repr__(self):
        return self._name

    def _handle_program_termination(self, stream):
        if self._process.poll() is None:
            return False
        self._fd_handler.unregister(stream)
        return True

    def _read_stream(self, name: str, stream):
        if self._handle_program_termination(stream):
            return

        print('%s: %s' % (name, stream.readline().decode().strip('\n')))


def main():
    fds = fd_handler()
    processes = []

    t0 = time.time()
    for l in json.load(open('processes.json'), encoding='utf-8'):
        for _ in range(l['count']):
            processes.append(
                process_handler(
                    name='p%d' % len(processes),
                    cmd=l['cmd'],
                    fd_handler=fds))

    print('start up took %.1fms' % ((time.time() - t0) * 1000),
          file=sys.stderr)

    while fds.size() > 0:
        fds.wait_and_process()

    print('execution took %.1fms' % ((time.time() - t0) * 1000),
          file=sys.stderr)

if __name__ == '__main__':
    main()
