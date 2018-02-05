from cement.core.controller import CementBaseController, expose
from cli.controllers.provider.enroll import ProviderEnrollController
from cli.controllers.provider.disenroll import ProviderDisenrollController
from cli.controllers.provider.server import ProviderServerController
from cli.controllers.provider.apps import ProviderAppsController


class ProviderController(CementBaseController):
  class Meta:
    label = 'provider'
    stacked_on = 'base'


  def _setup(self, app):
    super(ProviderController, self)._setup(app)
    app.handler.register(ProviderAppsController)
    app.handler.register(ProviderEnrollController)
    app.handler.register(ProviderDisenrollController)
    app.handler.register(ProviderServerController)
