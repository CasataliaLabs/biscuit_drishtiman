# usage repeatedTimer(1, fnName)

from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs

    def _run(self):
        self.function(*self.args, **self.kwargs)
        self.start()

    def start(self):
        self._timer = Timer(self.interval, self._run)
        self._timer.start()
         #   self.is_running = True

    def stop(self):
        self._timer.cancel()


