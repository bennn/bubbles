import os, signal, subprocess, threading

from log import Log
from timeoutException import TimeoutException

class TimedProcess(object):
    """
        2013-08-24:
            This is the work of a great man. A much greater man than I.
                http://stackoverflow.com/questions/1191374/subprocess-with-timeout/4825933#4825933
    """

    def __init__(self, cmd):
        self.cmd = cmd
        self.output = None, None
        self.process = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
            self.output = self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            os.killpg(self.process.pid, signal.SIGTERM)
            thread.join()
            raise TimeoutException
        else:
            return self.output
