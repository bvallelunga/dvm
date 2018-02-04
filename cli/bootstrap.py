from __future__ import absolute_import
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core.exc import CaughtSignal
import threading, traceback

from utils.store import store
from controllers import BaseController
from controllers.auth import AuthController
from controllers.provider import ProviderController


class App(CementApp):
  class Meta:
    label = 'app'
    base_controller = 'base'
    extensions = ['colorlog', 'tabulate']
    log_handler = 'colorlog'
    output_handler = 'tabulate'
    handlers = [
      BaseController,
      AuthController,
      ProviderController
    ]
    
  store = store

    
def main(args=None):
  try:
    app = App()
    app.setup()
    app.run()
  
  except CaughtSignal as e:
    for thread in threading.enumerate():
      className = thread.__class__.__name__

      if className == "Timer":
        thread.cancel()
    
    app.close()