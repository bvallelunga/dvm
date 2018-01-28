from cement.core.controller import CementBaseController, expose
from utils.services.provider import ProviderService
from datetime import datetime, timezone
from threading import Timer
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
    self.availability()
    
    server.run(
      host=self.app.pargs.host,
      port=int(self.app.pargs.port)
    )
  
  
  def availability(self):
    provider = ProviderService.availability(True)

    if provider:
      seconds_diff = (provider.available_expires_at - datetime.now(timezone.utc)).total_seconds()
      seconds = max(0, seconds_diff - config.provider_availability_buffer)
      thread = Timer(seconds, self.availability)
      thread.setName("cli.provider.availability")
      thread.start()
