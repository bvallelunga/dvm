from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from base import BaseController

class App(CementApp):
  class Meta:
    label = 'app'
    base_controller = 'base'
    handlers = [
      BaseController
    ]


"""The main routine."""
def main(args=None):
  with App() as app:
    app.run()
    
if __name__ == "__main__":
  main()
