from __future__ import absolute_import
from cement.core.controller import CementBaseController, expose
from cli.utils.services.provider import ProviderService
import cli.config as config


class AuthLoginController(CementBaseController):
  class Meta:
    label = 'login'
    stacked_on = 'auth'
    stacked_type = 'nested'
    usage = 'dvm login [arguments...]'
    description = 'Login by using your access token.'
    arguments = [
      (['--access-token', '-w'], dict(action='store', help="REQUIRED: Access Token", dest="access_token")),
      (['--endpoint', '-e'], dict(action='store', help="REQUIRED: Endpoint for Doppler to contact your server", dest="endpoint")),
    ]


  @expose(hide=True)
  def default(self):
    if not self.app.pargs.access_token:
      self.app.log.error("Access token field is missing")
      self.app.args.print_help()
      return


    if not self.app.pargs.endpoint:
        self.app.log.error("Endpoint field is missing")
        self.app.args.print_help()
        return

    old_access_token = self.app.store.get("access-token")
    old_provider = self.app.store.get("provider")
    self.app.store.set("access-token", self.app.pargs.access_token)

    provider = ProviderService.register(
        endpoint = "{}:{}".format(self.app.pargs.endpoint, config.provider_port)
    )

    if not provider:
        self.app.store.set("access-token", old_access_token)
        self.app.store.set("provider", old_provider)
        self.app.args.print_help()
        return

    self.app.store.set("provider", provider.id)
    self.app.store.set("apps", {})
    self.app.log.info("You have logged in successfully!")
