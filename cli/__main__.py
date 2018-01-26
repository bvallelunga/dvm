#! python3

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
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
  with App() as app:
    app.run()

   
if __name__ == "__main__":
  main()
