from __future__ import absolute_import
from cement.core.controller import CementBaseController, expose
from cli.utils.services.user import UserService
from cli.utils.services.provider import ProviderService
import webbrowser


class AuthRegisterController(CementBaseController):
  class Meta:
    label = 'register'
    stacked_on = 'auth'
    stacked_type = 'nested'
    usage = 'dvm register'
    description = 'Create a new user account'


  @expose(hide=True)
  def default(self):
      self.app.log.info("Welcome to Doppler, redirecting you to https://doppler.market/register to create an account.")
      webbrowser.open_new_tab("https://doppler.market/register")
