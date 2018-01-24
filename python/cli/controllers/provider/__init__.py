from cement.core.controller import CementBaseController, expose
from .enroll import ProviderEnrollController
from .disenroll import ProviderDisenrollController
from .server import ProviderServerController
from .apps import ProviderAppsController


class ProviderController(CementBaseController):
  class Meta:
    label = 'provider'
    stacked_on = 'base'
    stacked_type = 'nested'
    usage = 'dvm provider [command] [arguments...]'
    description = "Server management for executing tasks"


  def _setup(self, app):
    super(ProviderController, self)._setup(app)
    app.handler.register(ProviderAppsController)
    app.handler.register(ProviderEnrollController)
    app.handler.register(ProviderDisenrollController)
    app.handler.register(ProviderServerController)
    

  @expose(hide=True)
  def default(self):
    self.app.args.print_help()
