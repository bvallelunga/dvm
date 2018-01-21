#! python3

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from utils.store import Store

from controllers.base import BaseController
from controllers.auth import AuthController


class App(CementApp):
  class Meta:
    label = 'app'
    base_controller = 'base'
    extensions = ['colorlog']
    log_handler = 'colorlog'
    handlers = [
      BaseController,
      AuthController
    ]
  
  store = Store()

    
def main(args=None):
  with App() as app:
    app.run()

   
if __name__ == "__main__":
  main()
