from cement.core.controller import CementBaseController, expose
from utils.services.provider import ProviderService
import config, requests, os


class ProviderEnrollController(CementBaseController):
  class Meta:
    label = 'enroll'
    stacked_on = 'provider'
    stacked_type = 'nested'
    usage = 'dvm provider enroll [arguments...]'
    description = 'Enroll provider in apps'
    arguments = [
      (['--app', '-a'], dict(action='store', help="App ID to enroll in", dest="app")),
      (['--versions', '-v'], dict(action='store', help="Number of versions back to download", default=config.apps_supported_versions, dest="versions"))
    ]
   
  
  @expose(hide=True)
  def default(self): 
    app_id = self.app.pargs.app
       
    if not app_id:
      return self.app.log.error("Please provide an app id")
    
    apps_store = self.app.store.get("apps", {})
    app_store = apps_store[app_id] if app_id in apps_store else {}
    
    # Enroll app
    versions = int(self.app.pargs.versions)
    models = self.enroll_app()[0:versions]
    self.app.log.info("Enrolled in app {}".format(app_id))
    
    # Enroll models
    for model in models:
      self.enroll_model(model, app_store)
    
    # Finish
    apps_store[app_id] = app_store
    self.app.store.set("apps", apps_store)
    self.app.log.info("All models are downloaded and enrolled!")
  
  
  def enroll_app(self):
    return ProviderService.enroll_app(
      app = self.app,
      app_id = self.app.pargs.app,
      enroll = True
    ) or []
    
    
  def enroll_model(self, model, app_store):
    # Download tensorflow model
    response = requests.get(config.host + model.urls.tensorflow, stream=True, allow_redirects=True, headers={
      "access-token": self.app.store.get("access-token")
    })
    response.raise_for_status()
    fileName = "{}_{}_tensorflow.pb".format(model.app_id, model.version)
    filePath = os.path.join(config.local_directory, fileName)
    
    with open(filePath, 'wb') as f:
      for block in response.iter_content(1024):
        f.write(block) 
      f.close()
      
    app_store[model.version] = fileName
    
    # Enroll model
    ProviderService.enroll_model(
      app = self.app,
      app_id = model.app_id,
      version = model.version,
      enroll = True
    )
    
    self.app.log.info("Downloaded and enrolled in model {}".format(model.version))
