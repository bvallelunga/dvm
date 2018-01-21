from cement.core.controller import CementBaseController, expose


class AuthRegisterController(CementBaseController):
  class Meta:
    label = 'register'
    stacked_on = 'auth'
    stacked_type = 'nested'
    usage = 'dvm auth register [arguments...]'
    description = 'Create a new user account'
    arguments = [
      (['--name'], dict(action='store', help="OPTIONAL: Full Name")),
      (['--email'], dict(action='store', help="REQUIRED: Email Address")),
      (['--password'], dict(action='store', help="REQUIRED: Password")),
      (['--wallet'], dict(action='store', help="REQUIRED: DOP Wallet Address")),
    ]
   
  
  @expose(hide=True)
  def default(self):    
    print("Account created")

