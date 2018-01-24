from cement.core.controller import CementBaseController, expose
from utils.services.user import UserService
from utils.services.provider import ProviderService


class AuthRegisterController(CementBaseController):
  class Meta:
    label = 'register'
    stacked_on = 'auth'
    stacked_type = 'nested'
    usage = 'dvm auth register [arguments...]'
    description = 'Create new user account linked to your wallet address.'
    arguments = [
      (['--name', '-n'], dict(action='store', help="OPTIONAL: Full Name", dest="name")),
      (['--email', '-e'], dict(action='store', help="REQUIRED: Email Address", dest="email")),
      (['--password', '-p'], dict(action='store', help="REQUIRED: Password", dest="password")),
      (['--wallet', '-w'], dict(action='store', help="REQUIRED: DOP Wallet Address", dest="wallet")),
      (['--endpoint', '-ep'], dict(action='store', help="OPTIONAL: Endpoint for Doppler to contact your server", dest="endpoint")),
    ]
   
  
  @expose(hide=True)
  def default(self):  
    user = UserService.register(
      name = self.app.pargs.name,
      email = self.app.pargs.email,
      password = self.app.pargs.password,
      wallet = self.app.pargs.wallet
    )
    
    if not user: return
    self.app.store.set("access-token", user.wallet)
    provider = ProviderService.register(
      endpoint = self.app.pargs.endpoint 
    )
    
    if not provider: return
    self.app.store.set("provider", provider.id)
    self.app.store.set("apps", {})
    self.app.log.info("Account created, here is your access token: " + user.wallet)
    self.app.log.info("Your access token has been saved here: " + self.app.store.filePath) 
    self.app.log.info("Provider attached to your user account")
