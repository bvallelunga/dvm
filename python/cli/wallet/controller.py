from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose


class WalletController(CementBaseController):
  class Meta:
    label = 'wallet'
    stacked_on = 'base'
    stacked_type = 'nested'
    usage = 'dvm wallet [command] [arguments...]'
    description = "Create or load a wallet address"
    arguments = [
      (['arguments'], dict(action='store', nargs='*')),
    ]

  @expose(hide=True)
  def default(self):
    self.app.args.print_help()


  @expose(help="Register provided wallet with marketplace", aliases=["load [wallet address]"], aliases_only=True)
  def load(self):
    if len(self.app.pargs.arguments) == 0:
      self.app.log.error("Please provide a wallet address")
      return
      
    print("Wallet saved:", self.app.pargs.arguments[0])
    
  
  @expose(help="Generate wallet and register it with the marketplace")
  def create(self):    
    print("New wallet generated and saved: 0xC87238bF648C1aa1b64Ec83a0eCA4b8EB9E46F75")