#!/usr/bin/env python3

from __future__ import absolute_import
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core.exc import CaughtSignal
import threading, traceback

from cli.utils.store import store
from cli.controllers import BaseController
from cli.controllers.auth import AuthController
from cli.controllers.provider import ProviderController
from cli.controllers.provider import ProviderController
from cli.controllers.upgrade import UpgradeController


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
      ProviderController,
      UpgradeController
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
    
  except Exception as e:
    traceback.format_exc()
    

if __name__ == "__main__":
  main()