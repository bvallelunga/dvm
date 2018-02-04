#! python3

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core.exc import CaughtSignal
from utils.store import store
import threading, traceback

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
  except Exception as e:
    traceback.print_exc()
    
    for thread in threading.enumerate():
      className = thread.__class__.__name__

      if className == "Timer":
        thread.cancel()
    
    app.close()


   
if __name__ == "__main__":
  main()
