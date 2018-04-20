from __future__ import absolute_import
from cement.core.controller import CementBaseController, expose
from cli.controllers.auth.login import AuthLoginController
from cli.controllers.auth.register import AuthRegisterController
from cli.utils.services.provider import ProviderService
from cli.utils.services.wallet import WalletService


class AuthController(CementBaseController):
  class Meta:
    label = 'auth'
    stacked_on = 'base'


  def _setup(self, app):
    super(AuthController, self)._setup(app)
    app.handler.register(AuthRegisterController)
    app.handler.register(AuthLoginController)


  @expose(help="Your access token")
  def access_token(self):
    token = self.app.store.get("access-token")

    if token:
      self.app.log.info("Wallet Address: " + token)
    else:
      ProviderService.login_error()
