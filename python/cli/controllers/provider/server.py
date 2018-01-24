from cement.core.controller import CementBaseController, expose
import config

class ProviderServerController(CementBaseController):
  class Meta:
    label = 'server'
    stacked_on = 'provider'
    stacked_type = 'nested'
    usage = 'dvm provider server [arguments...]'
    description = 'Start provider server'
    arguments = [ 
      (['--port', '-p'], dict(action='store', help="Should match the endpoint's port from registration.", default=config.provider_port, dest="port"))
    ]
   
  
  @expose(hide=True)
  def default(self): 
    print(self.app.pargs.port)