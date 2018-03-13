from __future__ import absolute_import
from cement.core.controller import CementBaseController, expose
from cli.utils.services.provider import ProviderService
from cli.utils.services.app import AppService
import cli.config as config
import requests, os, shutil


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
      
    app = AppService.fetch(app_id)
    if not app: return self.app.log.error("App id invalid")
               
    if self.disenroll_app(app.id):
      self.delete_models(str(app.id))
      self.delete_models(app.slug)
      self.app.log.info("Disenrolled in app {}".format(app.slug))
    
  
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