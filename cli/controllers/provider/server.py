from __future__ import absolute_import
from cement.core.controller import CementBaseController, expose
from cli.utils.services.provider import ProviderService
from threading import Timer
import cli.server as server
import cli.config as config
import sys, signal, subprocess, os.path, datetime, os


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
      (['--ignore-checks'], dict(action='store_true', help="", dest="ignore_checks")),
      (['--flask-debug'], dict(action='store_true', help="Run flask in debug mode.", dest="flask_debug")),
      (['--force-upgrade'], dict(action='store_true', help="Force upgrade apps to newest version.", dest="force_upgrade"))
    ]
   
  
  @expose(hide=True)
  def default(self):
    # Force Upgrade Apps
    if self.app.pargs.force_upgrade:
      return self.update_models()
    
    # Kill Detached Server
    if self.app.pargs.kill:
      cmd = 'kill -9 `cat {}`;rm {}'.format(config.server_pid, config.server_pid)
      subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      self.app.log.info("Successfully killed detached server")
      sys.exit(0)
    
    # Check If a Detached Server Exists
    if not self.app.pargs.ignore_checks and os.path.isfile(config.server_pid):
      self.app.log.error("A detached server already exists. Please kill it [dvm server --kill] if you would like to create another server.")
      sys.exit(0)
    
    # Deteched Server
    if self.app.pargs.detached:
      cmd = 'nohup dvm server --host={} --port={} --ignore-checks > {} 2> {} & echo $! > {}'.format(
        self.app.pargs.host, 
        self.app.pargs.port, 
        config.server_error_log, 
        config.server_out_log,
        config.server_pid
      )
      subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      self.app.log.info("Started detached server!")
      sys.exit(0)
    
    # Non Detached Server
    apps = self.app.store.get("apps", {})
    
    if len(apps.keys()) == 0:
      return self.app.log.error("Please enroll in at least one app first.\n$ dvm provider enroll")
    
    # If is detached server
    if True or self.app.pargs.ignore_checks:
      self.update_models_timer() 
    
    self.availability_ping()
    self.start_server()
  
   
  def availability_ping(self):
    provider = ProviderService.availability(True)
    if not provider: sys.exit(0)
        
    seconds_diff = (provider.available_expires_at - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
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
  
  
  def update_models_timer(self):
    date_format = "%Y-%m-%d %H:%M:%S"
    tomorrow_string = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)).strftime(date_format)
    diff_date = datetime.datetime.strptime(self.app.store.get("update_models_time", tomorrow_string), date_format).replace(tzinfo=datetime.timezone.utc)
    self.app.store.set("update_models_time", diff_date.strftime(date_format)) 
    
    diff_seconds = (diff_date - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
    thread = Timer(diff_seconds, self.update_models)
    thread.setName("cli.provider.update_models_timer")
    thread.start()
    
  
  def update_models(self):
    self.app.log.info("Updating apps to newest version")
    self.app.store.delete("update_models_time")
    apps_store = self.app.store.get("apps", {})
    app_slugs = apps_store.keys()
    
    kill_cmd = "dvm server --kill"
    disenroll_cmd = str.join(";", [ "dvm disenroll --app {}".format(slug) for slug in app_slugs ])
    enroll_cmd = str.join(";", [ "dvm enroll --app {}".format(slug) for slug in app_slugs ])
    start_cmd = "dvm server --detached"
    cmd = str.join(";", [ kill_cmd, disenroll_cmd, enroll_cmd, start_cmd ])
    
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
      output = process.stdout.readline()
      if output == '' or process.poll() is not None:
        break
      if output:
        print(output.strip().decode('ascii'))
    
    process.poll()
    sys.exit(0)


  def tomorrow(self):
    return datetime.timedelta(days=1).total_seconds()
