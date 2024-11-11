from subprocess import Popen, PIPE
import select
import fcntl, os
import time

class Communicator(object):
    def __init__(self, command,timeout):
        self.timeout = timeout
        self.process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)
        fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        self.accumulated_time = 0

    def send(self, data, tail = '\n'.encode()):
        self.process.stdin.write(data + tail)
        self.process.stdin.flush()
        time.sleep(0.01)

    def recv(self,t=0.2,return_stderr=False,time_already=None):
        if time_already is not None:
            DeprecationWarning("time_already parameter has been deprecated, and it will be removed soon.")
        r = ''
        pr = self.process.stdout
        per = self.process.stderr
        bt = time.time()
        er = b''
        while ((time.time() - bt)+self.accumulated_time < self.timeout):
            if not select.select([pr], [], [], 0)[0]:
                time.sleep(t)
                continue

            r = pr.read().rstrip()
            self.accumulated_time += time.time() - bt
            if r.decode() == ' ' or r.decode() == '':
                er = per.read()
            if return_stderr:
                return r,er
            return r
        raise TimeoutError
