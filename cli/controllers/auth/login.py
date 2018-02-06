from __future__ import absolute_import
from cement.core.controller import CementBaseController, expose
from cli.utils.services.provider import ProviderService


class AuthLoginController(CementBaseController):
  class Meta:
    label = 'login'
    stacked_on = 'auth'
    stacked_type = 'nested'
    usage = 'dvm login [arguments...]'
    description = 'Login by using your wallet address. If a provider id is not given, an account will be created.'
    arguments = [
      (['--wallet', '-w'], dict(action='store', help="REQUIRED: DOP Wallet Address", dest="wallet")),
      (['--endpoint', '-e'], dict(action='store', help="OPTIONAL: Endpoint for Doppler to contact your server", dest="endpoint")),
      (['--provider', '-p'], dict(action='store', help="OPTIONAL: Provider ID, must be owned by the wallet", dest="provider")),
    ]
   
  
  @expose(hide=True)
  def default(self):    
    if not self.app.pargs.wallet:
      self.app.log.error("Wallet address is missing")
      self.app.args.print_help()
      return
    
    old_access_token = self.app.store.get("access-token")
    old_provider = self.app.store.get("provider")
    self.app.store.set("access-token", self.app.pargs.wallet)
    
    if self.app.pargs.provider:
      self.app.store.set("provider", self.app.pargs.provider) 
    
    else:
      provider = ProviderService.register(
        endpoint = self.app.pargs.endpoint 
      )
      
      if not provider: 
        self.app.store.set("access-token", old_access_token)
        self.app.store.set("provider", old_provider)
        self.app.args.print_help()
        return
      
      self.app.store.set("provider", provider.id)
    
    self.app.store.set("apps", {})
    self.app.log.info("Wallet address stored locally")
    self.app.log.info("Provider attached to your user account")