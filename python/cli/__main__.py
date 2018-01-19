from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

from base.controller import BaseController
from wallet.controller import WalletController

class App(CementApp):
  class Meta:
    label = 'app'
    base_controller = 'base'
    extensions = ['colorlog']
    log_handler = 'colorlog'
    handlers = [
      BaseController,
      WalletController
    ]


def main(args=None):
  with App() as app:
    app.run()

   
if __name__ == "__main__":
  main()
