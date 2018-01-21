from cement.core.controller import CementBaseController, expose
from .login import AuthLoginController
from .register import AuthRegisterController
from utils.services.provider import ProviderService


class AuthController(CementBaseController):
  class Meta:
    label = 'auth'
    stacked_on = 'base'
    stacked_type = 'nested'
    usage = 'dvm auth [command] [arguments...]'
    description = "User authentication and management"

  
  def _setup(self, app):
    super(AuthController, self)._setup(app)
    app.handler.register(AuthRegisterController)
    app.handler.register(AuthLoginController)


  @expose(hide=True)
  def default(self):
    self.app.args.print_help()
    
  
  @expose(help="Generate a DOP wallet address")
  def generate_wallet(self):
    print("New wallet generated: 0xC87238bF648C1aa1b64Ec83a0eCA4b8EB9E46F75")
    