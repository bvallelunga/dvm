from cement.core.controller import CementBaseController, expose
from utils.services.provider import ProviderService
import config, requests, os, shutil


class ProviderDisenrollController(CementBaseController):
  class Meta:
    label = 'disenroll'
    stacked_on = 'provider'
    stacked_type = 'nested'
    usage = 'dvm disenroll [arguments...]'
    description = 'Disenroll provider in app'
    arguments = [
      (['--app', '-a'], dict(action='store', help="App ID to enroll in", dest="app")),
    ]
   
  
  @expose(hide=True)
  def default(self): 
    app_id = self.app.pargs.app
    
    if not app_id:
      return self.app.log.error("Please provide an app id")
           
    if self.disenroll_app(app_id):
      self.delete_models(app_id)
      self.app.log.info("Disenrolled in app {}".format(app_id))
    
  
  def disenroll_app(self, app_id):    
    return ProviderService.enroll_app(
      app_id = app_id,
      enroll = False
    )
    
    
  def delete_models(self, app_id):
    apps_store = self.app.store.get("apps", {})
    appFolder = os.path.join(config.app_store, app_id)
    shutil.rmtree(appFolder, ignore_errors=True)
    
    if app_id in apps_store:         
      del apps_store[app_id]
      self.app.store.set("apps", apps_store)