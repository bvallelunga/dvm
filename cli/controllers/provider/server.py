from cement.core.controller import CementBaseController, expose
from server import server
import config

class ProviderServerController(CementBaseController):
  class Meta:
    label = 'server'
    stacked_on = 'provider'
    stacked_type = 'nested'
    usage = 'dvm provider server [arguments...]'
    description = 'Start provider server'
    arguments = [ 
      (['--host'], dict(action='store', help="Should be accessible to the public.", default=config.provider_host, dest="host")),
      (['--port'], dict(action='store', help="Should match the endpoint's port from registration.", default=config.provider_port, dest="port"))
    ]
   
  
  @expose(hide=True)
  def default(self):
    server.run(
      host=self.app.pargs.host,
      port=int(self.app.pargs.port)
    )