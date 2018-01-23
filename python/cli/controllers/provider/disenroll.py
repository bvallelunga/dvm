from cement.core.controller import CementBaseController, expose
from utils.services.provider import ProviderService
import config, requests, os


class ProviderDisenrollController(CementBaseController):
  class Meta:
    label = 'disenroll'
    stacked_on = 'provider'
    stacked_type = 'nested'
    usage = 'dvm provider disenroll [arguments...]'
    description = 'Disenroll provider in apps'
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
      app = self.app,
      app_id = app_id,
      enroll = False
    )
    
    
  def delete_models(self, app_id):
    apps_store = self.app.store.get("apps", {})
    
    if app_id in apps_store:   
      for key, value in apps_store[app_id].items():
        os.remove(os.path.join(config.local_directory, value))
      
      del apps_store[app_id]
      self.app.store.set("apps", apps_store)