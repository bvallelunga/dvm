from cement.core.controller import CementBaseController, expose
from utils.services.provider import ProviderService


class AuthLoginController(CementBaseController):
  class Meta:
    label = 'login'
    stacked_on = 'auth'
    stacked_type = 'nested'
    usage = 'dvm auth login [arguments...]'
    description = 'Login by using a wallet address'
    arguments = [
      (['--wallet', '-w'], dict(action='store', help="DOP Wallet Address", dest="wallet")),
      (['--endpoint', '-e'], dict(action='store', help="Endpoint for Doppler Servers", dest="endpoint"))
    ]
   
  
  @expose(hide=True)
  def default(self):    
    if not self.app.pargs.wallet:
      self.app.log.error("Wallet address is missing")
      return
    
    old_access_token = self.app.store.get("access-token")
    old_provider = self.app.store.get("provider")
    self.app.store.set("access-token", self.app.pargs.wallet)
    
    provider = ProviderService.register(
      app = self.app,
      endpoint = self.app.pargs.endpoint 
    )
    
    if not provider: 
      self.app.store.set("access-token", old_access_token)
      self.app.store.set("provider", old_provider)
      return
    
    self.app.store.set("provider", provider.id)
    self.app.log.info("Wallet address stored locally")
    self.app.log.info("Provider attached to your user account")