from cement.core.controller import CementBaseController, expose
from utils.services.user import UserService


class AuthRegisterController(CementBaseController):
  class Meta:
    label = 'register'
    stacked_on = 'auth'
    stacked_type = 'nested'
    usage = 'dvm auth register [arguments...]'
    description = 'Create a new user account'
    arguments = [
      (['--name'], dict(action='store', help="OPTIONAL: Full Name", dest="name")),
      (['--email'], dict(action='store', help="REQUIRED: Email Address", dest="email")),
      (['--password'], dict(action='store', help="REQUIRED: Password", dest="password")),
      (['--wallet'], dict(action='store', help="REQUIRED: DOP Wallet Address", dest="wallet")),
    ]
   
  
  @expose(hide=True)
  def default(self):    
    response = UserService.register(
      app = self.app,
      name = self.app.pargs.name,
      email = self.app.pargs.email,
      password = self.app.pargs.password,
      wallet = self.app.pargs.wallet
    )
    
    if not response: return
    self.app.store.set("access-token", response.wallet)
    self.app.log.info("Account created, here is your access token: " + response.wallet)
    self.app.log.info("Your access token has been saved here: " + self.app.store.filePath) 
