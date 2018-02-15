from __future__ import absolute_import
from cement.core.controller import CementBaseController, expose
from cli.utils.services.provider import ProviderService
from datetime import datetime, timezone
from threading import Timer
import cli.server as server
import cli.config as config
import sys, signal, subprocess, os.path


class ProviderServerController(CementBaseController):
  class Meta:
    label = 'server'
    stacked_on = 'provider'
    stacked_type = 'nested'
    usage = 'dvm server [arguments...]'
    description = 'Start provider server'
    arguments = [ 
      (['--host'], dict(action='store', help="Should be accessible to the public.", default=config.provider_host, dest="host")),
      (['--port'], dict(action='store', help="Should match the endpoint's port from registration.", default=config.provider_port, dest="port")),
      (['--detached'], dict(action='store_true', help="Run server in background mode.", dest="detached")),
      (['--kill'], dict(action='store_true', help="Kill an active detached server.", dest="kill")),
      (['--flask-debug'], dict(action='store_true', help="Run flask in debug mode.", dest="flask_debug"))
    ]
   
  
  @expose(hide=True)
  def default(self):
    # Kill Detached Server
    if self.app.pargs.kill:
      cmd = 'kill -9 `cat {}`;rm {}'.format(config.server_pid, config.server_pid)
      process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      self.app.log.info("Successfully killed detached server")
      sys.exit(0)
    
    # Check If a Detached Server Exists
    if os.path.isfile(config.server_pid):
      self.app.log.error("A detached server already exists. Please kill it [dvm server --kill] if you would like to create another server.")
      sys.exit(0)
    
    # Deteched Server
    if self.app.pargs.detached:
      cmd = 'nohup dvm server --host={} --port={} > {} 2> {} & echo $! > {}'.format(
        self.app.pargs.host, 
        self.app.pargs.port, 
        config.server_out_log, 
        config.server_error_log,
        config.server_pid
      )
      process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      self.app.log.info("Started detached server!")
      sys.exit(0)
    
    # Non Detached Server
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