from cement.core.controller import CementBaseController, expose
from utils.services.app import AppService

class ProviderAppsController(CementBaseController):
  class Meta:
    label = 'apps'
    stacked_on = 'provider'
    stacked_type = 'nested'
    usage = 'dvm provider apps'
    description = 'Your enrolled apps'
   
  
  @expose(hide=True)
  def default(self): 
    apps_store = self.app.store.get("apps", {})
    app_keys = apps_store.keys()
    
    if len(app_keys) == 0:
      return self.app.log.error("You have not enrolled in any apps")
    
    headers=['ID', 'NAME', 'DESCRIPTION', 'VERSIONS', 'PROVIDERS']
    data=[]
    
    for id in app_keys:
      app = AppService.fetch(id)
      if app: 
        data.append([
          app.id,
          app.name,
          app.description,
          app.versions,
          app.enrolled_providers
        ])
    
    self.app.render(data, headers=headers)
    