from cement.core.controller import CementBaseController, expose
from .enroll import ProviderEnrollController
from .disenroll import ProviderDisenrollController
from .server import ProviderServerController
from .apps import ProviderAppsController


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
