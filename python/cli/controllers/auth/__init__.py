from cement.core.controller import CementBaseController, expose
from .register import AuthRegisterController
from utils.services.user import UserService


class AuthController(CementBaseController):
  class Meta:
    label = 'auth'
    stacked_on = 'base'
    stacked_type = 'nested'
    usage = 'dvm auth [command] [arguments...]'
    description = "User authentication and management"
    arguments = [
      (['arguments'], dict(action='store', nargs='*')),
    ]
    
  
  def _setup(self, app):
    super(AuthController, self)._setup(app)
    app.handler.register(AuthRegisterController)


  @expose(hide=True)
  def default(self):
    self.app.args.print_help()
    
  
  @expose(help="Generate a DOP wallet address")
  def generate_wallet(self):
    print("New wallet generated: 0xC87238bF648C1aa1b64Ec83a0eCA4b8EB9E46F75")
    
    
  @expose(help="Login by using a wallet address", aliases=["login [wallet]"], aliases_only=True)
  def login(self):    
    if len(self.app.pargs.arguments) == 0:
      self.app.log.error("Wallet address is missing")
      return
      
    print("Wallet logged in:", self.app.pargs.arguments[0])