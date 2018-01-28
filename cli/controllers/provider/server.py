from cement.core.controller import CementBaseController, expose
from utils.services.provider import ProviderService
from datetime import datetime, timezone
from threading import Timer
from server import server
import sys
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
      (['--port'], dict(action='store', help="Should match the endpoint's port from registration.", default=config.provider_port, dest="port")),
      (['--flask-debug'], dict(action='store_true', help="", default=config.provider_port, dest="flask_debug"))
    ]
   
  
  @expose(hide=True)
  def default(self):
    apps = self.app.store.get("apps", {})
    
    if len(apps.keys()) == 0:
      return self.app.log.error("Please enroll in at least one app first.\n$ dvm provider enroll")
    
    self.availability_ping()
    self.start_server()
  
   
  def availability_ping(self):
    provider = ProviderService.availability(True)

    if not provider: sys.exit(0)
        
    seconds_diff = (provider.available_expires_at - datetime.now(timezone.utc)).total_seconds()
    seconds = max(0, seconds_diff - config.provider_availability_buffer)
    thread = Timer(seconds, self.availability_ping)
    thread.setName("cli.provider.availability")
    thread.start()


  def start_server(self):
    server.run(
      host=self.app.pargs.host,
      port=int(self.app.pargs.port),
      debug=self.app.pargs.flask_debug
    )