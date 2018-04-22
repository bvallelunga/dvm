from __future__ import absolute_import
from cement.core.controller import CementBaseController, expose
from cli.utils.services.app import AppService

class ProviderAppsController(CementBaseController):
  class Meta:
    label = 'apps'
    stacked_on = 'provider'
    stacked_type = 'nested'
    usage = 'dvm apps'
    description = 'Your enrolled apps'
   
  
  @expose(hide=True)
  def default(self): 
    apps_store = self.app.store.get("apps", {})
    app_keys = apps_store.keys()
    
    if len(app_keys) == 0:
      return self.app.log.error("Please enroll in at least one app first.\n$ dvm provider enroll")
    
    headers=['SLUG', 'DESCRIPTION', 'VERSIONS', 'PROVIDERS']
    data=[]
    
    for id in app_keys:
      app = AppService.fetch(id)
      print(123)
      if app: 
        data.append([
          app.slug,
          app.description_short,
          app.versions,
          app.enrolled_providers
        ])
    
    self.app.render(data, headers=headers)
    