# Code from StackOverflow
# https://stackoverflow.com/questions/28635985/extending-threading-timer-for-returning-value-from-function-gives-typeerror

from threading import Timer as Timer

class ReturnTimer(Timer):
  def __init__(self, interval, function, args=[], kwargs={}):
    self._original_function = function
    super(ReturnTimer, self).__init__(
      interval, self._do_execute, args, kwargs)

  def _do_execute(self, *a, **kw):
    self.result = self._original_function(*a, **kw)

  def start(self):
    super(ReturnTimer, self).start()
    self.join()
    return self.result
